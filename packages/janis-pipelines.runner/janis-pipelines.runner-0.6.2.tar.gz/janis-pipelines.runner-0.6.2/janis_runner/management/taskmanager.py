"""
I think this is where the bread and butter is!

A task manager will have reference to a database,


"""
import os
import json
import time
from datetime import datetime
from subprocess import call
from typing import Optional, List, Dict

from janis_core.workflow.workflow import Workflow
from janis_core.translations import get_translator
from janis_core.translations.translationbase import TranslatorBase

from janis_runner.data.providers.task.dbmanager import TaskDbManager
from janis_runner.data.enums import InfoKeys, ProgressKeys
from janis_runner.data.models.filescheme import FileScheme
from janis_runner.data.models.schema import TaskStatus, TaskMetadata, JobMetadata
from janis_runner.engines import get_ideal_specification_for_engine, Cromwell, CWLTool
from janis_runner.engines.cromwell import CromwellFile
from janis_runner.environments.environment import Environment
from janis_runner.utils import get_extension, Logger
from janis_runner.validation import (
    generate_validation_workflow_from_janis,
    ValidationRequirements,
)


class TaskManager:
    def __init__(self, outdir: str, tid: str, environment: Environment = None):
        # do stuff here
        self.tid = tid

        # hydrate from here if required
        self._engine_tid = None
        self.path = outdir
        self.outdir_workflow = (
            self.get_task_path() + "workflow/"
        )  # handy to have as reference
        self.create_dir_structure(self.path)

        self.database = TaskDbManager(self.get_task_path_safe())
        self.environment = environment

        if not self.tid:
            self.tid = self.get_engine_tid()

    def has(
        self,
        status: Optional[TaskStatus],
        name: Optional[str] = None,
        environment: Optional[str] = None,
    ):
        has = True
        if status:
            has = has and self.database.get_meta_info(InfoKeys.status) == status
        if name:
            has = has and self.database.get_meta_info(InfoKeys.name).lower().startswith(
                name.lower()
            )
        return has

    @staticmethod
    def from_janis(
        tid: str,
        outdir: str,
        wf: Workflow,
        environment: Environment,
        hints: Dict[str, str],
        validation_requirements: Optional[ValidationRequirements],
        inputs_dict: dict = None,
        dryrun=False,
        watch=True,
        show_metadata=True,
        max_cores=None,
        max_memory=None,
        keep_intermediate_files=False,
    ):

        # output directory has been created

        environment.identifier += "_" + tid

        tm = TaskManager(tid=tid, outdir=outdir, environment=environment)
        tm.database.add_meta_infos(
            [
                (InfoKeys.taskId, tid),
                (InfoKeys.status, TaskStatus.PROCESSING),
                (InfoKeys.validating, validation_requirements is not None),
                (InfoKeys.engineId, environment.engine.id()),
                (InfoKeys.fileschemeId, environment.filescheme.identifier),
                (InfoKeys.environment, environment.id()),
                (InfoKeys.name, wf.id()),
                (InfoKeys.start, datetime.now().isoformat()),
                (InfoKeys.executiondir, None),
                (InfoKeys.keepExecDir, keep_intermediate_files),
            ]
        )
        tm.database.persist_engine(environment.engine)
        tm.database.persist_filescheme(environment.filescheme)

        spec = get_ideal_specification_for_engine(environment.engine)
        spec_translator = get_translator(spec)
        wf_evaluate = tm.prepare_and_output_workflow_to_evaluate_if_required(
            workflow=wf,
            translator=spec_translator,
            validation=validation_requirements,
            hints=hints,
            additional_inputs=inputs_dict,
            max_cores=max_cores,
            max_memory=max_memory,
        )

        if not dryrun:
            # this happens for all workflows no matter what type
            tm.database.update_meta_info(InfoKeys.status, TaskStatus.QUEUED)
            tm.submit_workflow_if_required(wf_evaluate, spec_translator)
            if watch:
                tm.resume_if_possible(show_metadata=show_metadata)
        else:
            tm.database.update_meta_info(InfoKeys.status, "DRY-RUN")

        return tm

    @staticmethod
    def from_path(path, config_manager):
        """
        :param config_manager:
        :param path: Path should include the $tid if relevant
        :return: TaskManager after resuming (might include a wait)
        """
        # get everything and pass to constructor
        # database path

        path = TaskManager.get_task_path_for(path)
        db = TaskDbManager(path)

        tid = db.get_meta_info(InfoKeys.taskId)
        envid = db.get_meta_info(InfoKeys.environment)
        eng = db.get_engine()
        fs = db.get_filescheme()
        env = Environment(envid, eng, fs)

        db.close()

        tm = TaskManager(outdir=path, tid=tid, environment=env)
        return tm

    def resume_if_possible(self, show_metadata=True):
        # check status and see if we can resume
        if not self.database.progress_has_completed(ProgressKeys.submitWorkflow):
            return Logger.critical(
                f"Can't resume workflow with id '{self.tid}' as the workflow "
                "was not submitted to the engine"
            )
        self.wait_if_required(show_metadata=show_metadata)
        self.save_metadata_if_required()
        self.copy_outputs_if_required()
        self.remove_exec_dir()
        self.environment.engine.stop_engine()

        print(
            f"Finished managing task '{self.tid}'. View the task outputs: file://{self.get_task_path()}"
        )
        return self

    def prepare_and_output_workflow_to_evaluate_if_required(
        self,
        workflow,
        translator: TranslatorBase,
        validation: ValidationRequirements,
        hints: Dict[str, str],
        additional_inputs: dict,
        max_cores=None,
        max_memory=None,
    ):
        if self.database.progress_has_completed(ProgressKeys.saveWorkflow):
            return Logger.info(f"Saved workflow from task '{self.tid}', skipping.")

        Logger.log(f"Saving workflow with id '{workflow.id()}'")

        translator.translate(
            workflow,
            to_console=False,
            to_disk=True,
            with_resource_overrides=True,
            merge_resources=True,
            hints=hints,
            write_inputs_file=True,
            export_path=self.outdir_workflow,
            additional_inputs=additional_inputs,
            max_cores=max_cores,
            max_mem=max_memory,
        )

        Logger.log(
            f"Saved workflow with id '{workflow.id()}' to '{self.outdir_workflow}'"
        )

        workflow_to_evaluate = workflow
        if validation:
            Logger.log(
                f"Validation requirements provided, wrapping workflow '{workflow.id()}' with hap.py"
            )

            # we need to generate both the validation and non-validation workflow
            workflow_to_evaluate = generate_validation_workflow_from_janis(
                workflow, validation
            )

            wid = workflow.id()

            adjusted_inputs = (
                {wid + "_" + k: v for k, v in additional_inputs.items()}
                if additional_inputs
                else None
            )

            translator.translate(
                workflow_to_evaluate,
                to_console=False,
                to_disk=True,
                with_resource_overrides=True,
                merge_resources=True,
                hints=hints,
                write_inputs_file=True,
                export_path=self.outdir_workflow,
                additional_inputs=adjusted_inputs,
                max_cores=max_cores,
                max_mem=max_memory,
            )

        self.database.progress_mark_completed(ProgressKeys.saveWorkflow)
        return workflow_to_evaluate

    def submit_workflow_if_required(self, wf, translator):
        if self.database.progress_has_completed(ProgressKeys.submitWorkflow):
            return Logger.log(f"Workflow '{self.tid}' has submitted finished, skipping")

        fn_wf = self.outdir_workflow + translator.workflow_filename(wf)
        fn_inp = self.outdir_workflow + translator.inputs_filename(wf)
        fn_deps = self.outdir_workflow + translator.dependencies_filename(wf)

        Logger.log(f"Submitting task '{self.tid}' to '{self.environment.engine.id()}'")
        self._engine_tid = self.environment.engine.start_from_paths(
            self.tid, fn_wf, fn_inp, fn_deps
        )
        self.database.add_meta_info(InfoKeys.engine_tid, self._engine_tid)
        Logger.log(
            f"Submitted workflow ({self.tid}), got engine id = '{self.get_engine_tid()}'"
        )

        self.database.progress_mark_completed(ProgressKeys.submitWorkflow)

    def save_metadata_if_required(self):
        if self.database.progress_has_completed(ProgressKeys.savedMetadata):
            return Logger.log(f"Workflow '{self.tid}' has saved metadata, skipping")

        if isinstance(self.environment.engine, Cromwell):
            import json

            meta = self.environment.engine.raw_metadata(self.get_engine_tid()).meta
            with open(self.get_task_path() + "metadata/metadata.json", "w+") as fp:
                json.dump(meta, fp)

        elif isinstance(self.environment.engine, CWLTool):
            import json

            meta = self.environment.engine.metadata(self.tid)
            self.database.update_meta_info(InfoKeys.status, meta.status)
            with open(self.get_task_path() + "metadata/metadata.json", "w+") as fp:
                json.dump(meta.outputs, fp)

        else:
            raise Exception(
                f"Don't know how to save metadata for engine '{self.environment.engine.id()}'"
            )

        self.database.progress_mark_completed(ProgressKeys.savedMetadata)

    def copy_outputs_if_required(self):
        if self.database.progress_has_completed(ProgressKeys.copiedOutputs):
            return Logger.log(f"Workflow '{self.tid}' has copied outputs, skipping")

        outputs = self.environment.engine.outputs_task(self.get_engine_tid())
        if not outputs:
            return

        is_validating = bool(self.database.get_meta_info(InfoKeys.validating))
        outdir = self.get_task_path() + "outputs/"
        valdir = self.get_task_path() + "validation/"

        def output_is_validating(o):
            return is_validating and o.split(".")[-1].startswith("validated_")

        fs = self.environment.filescheme

        with open(outdir + "outputs.json", "w+") as oofp:
            json.dump(dict(outputs), oofp)

        for outname, o in outputs.items():

            od = valdir if output_is_validating(outname) else outdir

            if isinstance(o, list):
                self.copy_sharded_outputs(fs, od, outname, o)
            elif isinstance(o, CromwellFile):
                self.copy_cromwell_output(fs, od, outname, o)
            elif isinstance(o, str):
                self.copy_output(fs, od, outname, o)

            else:
                raise Exception(f"Don't know how to handle output with type: {type(o)}")

        self.database.progress_mark_completed(ProgressKeys.copiedOutputs)

    def wait_if_required(self, show_metadata=True):

        if self.database.progress_has_completed(ProgressKeys.workflowMovedToFinalState):
            try:
                meta = self.metadata()
                if meta:
                    print(meta.format())
            except:
                print("Failed to get metadata, but skipping because task has finished")

            return Logger.log(f"Workflow '{self.tid}' has already finished, skipping")

        status = None

        while status not in TaskStatus.final_states():
            meta = self.metadata()
            if meta:
                if show_metadata:
                    call("clear")
                    print(meta.format())
                status = meta.status
                infos = [(InfoKeys.status, status)]
                if meta.executionDir:
                    infos.append((InfoKeys.executiondir, meta.executionDir))
                self.database.update_meta_infos(infos)

            if status not in TaskStatus.final_states():
                time.sleep(5)

        self.database.add_meta_info(InfoKeys.finish, datetime.now().isoformat())
        self.database.progress_mark_completed(ProgressKeys.workflowMovedToFinalState)

    def remove_exec_dir(self):
        status = self.database.get_meta_info(InfoKeys.status)

        keep_intermediate = (
            self.database.get_meta_info(InfoKeys.keepExecDir).lower() == "true"
        )
        if (
            not keep_intermediate
            and status is not None
            and status == str(TaskStatus.COMPLETED)
        ):
            execdir = self.database.get_meta_info(InfoKeys.executiondir)
            if execdir and execdir != "None":
                Logger.info("Cleaning up execution directory")
                self.environment.filescheme.rm_dir(execdir)
                self.database.progress_mark_completed(ProgressKeys.cleanedUp)

    def log_dbtaskinfo(self):
        import tabulate

        # log all the metadata we have:
        results = self.database.get_all_meta_info()
        header = ("Key", "Value")
        res = tabulate.tabulate([header, ("tid", self.tid), *results.items()])
        print(res)
        return res

    @staticmethod
    def copy_output(filescheme: FileScheme, output_dir, filename, source):

        if isinstance(source, list):
            TaskManager.copy_sharded_outputs(filescheme, output_dir, filename, source)
        elif isinstance(source, CromwellFile):
            TaskManager.copy_cromwell_output(filescheme, output_dir, filename, source)
        elif isinstance(source, str):
            ext = get_extension(source)
            extwdot = ("." + ext) if ext else ""
            filescheme.cp_from(source, output_dir + filename + extwdot, None)

    @staticmethod
    def copy_sharded_outputs(
        filescheme: FileScheme, output_dir, filename, outputs: List[CromwellFile]
    ):
        for counter in range(len(outputs)):
            sid = f"-shard-{counter}"
            TaskManager.copy_output(
                filescheme, output_dir, filename + sid, outputs[counter]
            )

    @staticmethod
    def copy_cromwell_output(
        filescheme: FileScheme, output_dir: str, filename: str, out: CromwellFile
    ):
        TaskManager.copy_output(filescheme, output_dir, filename, out.location)
        if out.secondary_files:
            for sec in out.secondary_files:
                TaskManager.copy_output(filescheme, output_dir, filename, sec.location)

    def get_engine_tid(self):
        if not self._engine_tid:
            self._engine_tid = self.database.get_meta_info(InfoKeys.engine_tid)
        return self._engine_tid

    def get_task_path(self):
        return TaskManager.get_task_path_for(self.path)

    @staticmethod
    def get_task_path_for(outdir: str):
        return outdir

    def get_task_path_safe(self):
        path = self.get_task_path()
        TaskManager._create_dir_if_needed(path)
        return path

    @staticmethod
    def create_dir_structure(path):
        outputdir = TaskManager.get_task_path_for(path)
        folders = [
            "workflow",
            "metadata",
            "validation",
            "outputs",
            "logs",
            "configuration",
            "execution",
        ]
        TaskManager._create_dir_if_needed(path)

        # workflow folder
        for f in folders:
            TaskManager._create_dir_if_needed(os.path.join(outputdir, f))

    def copy_logs_if_required(self):
        if not self.database.progress_has_completed(ProgressKeys.savedLogs):
            return Logger.log(f"Workflow '{self.tid}' has copied logs, skipping")

        meta = self.metadata()

    @staticmethod
    def get_logs_from_jobs_meta(meta: List[JobMetadata]):
        ms = []

        for j in meta:
            ms.append((f"{j.jobid}-stderr", j.stderr))
            ms.append((f"{j.jobid}-stdout", j.stderr))

    def watch(self):
        import time
        from subprocess import call

        status = None

        while status not in TaskStatus.final_states():
            meta = self.metadata()
            if meta:
                call("clear")

                print(meta.format())
                status = meta.status
            if status not in TaskStatus.final_states():
                time.sleep(2)

    def metadata(self) -> TaskMetadata:
        meta = self.environment.engine.metadata(self.get_engine_tid())
        if meta:
            meta.name = self.database.get_meta_info(InfoKeys.name)
            meta.tid = self.tid
            meta.outdir = self.path
            meta.engine_name = str(self.environment.engine.engtype)
            meta.engine_url = (
                self.environment.engine.host
                if isinstance(self.environment.engine, Cromwell)
                else "N/A"
            )
        return meta

    def abort(self) -> bool:
        self.database.update_meta_info(InfoKeys.status, TaskStatus.TERMINATED)
        status = False
        try:
            status = bool(self.environment.engine.terminate_task(self.get_engine_tid()))
        except Exception as e:
            Logger.critical("Couldn't abort task from engine: " + str(e))
        try:
            self.environment.engine.stop_engine()
        except Exception as e:
            Logger.critical("Couldn't stop engine: " + str(e))

        return status

    @staticmethod
    def _create_dir_if_needed(path):
        if not os.path.exists(path):
            os.makedirs(path)

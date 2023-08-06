from typing import Optional, Dict
import os.path
import subprocess

from .program_arguments import ProgramArguments
from .project_reader import read_project_definition, ProjectDefinition, parse_file_name, ParsedFile
from .file_resolver import FileResolver


def process_folder(current_path: str,
                   file_resolver: FileResolver,
                   project_parameters: Dict[str, str],
                   path_mappings: Dict[str, str]) -> None:
    """
    Recursively process the handlebars templates for the given project.
    """
    for file_entry in file_resolver.listdir():
        file: ParsedFile = parse_file_name(file_entry.name, project_parameters)
        full_local_path = os.path.join(current_path, file.name)

        if file_entry.name == "HELP.md" or file_entry.name == ".ars":
            continue

        path_mappings[os.path.normpath(full_local_path)] = os.path.normpath(file_entry.absolute_path)

        if file_entry.is_dir:
            process_folder(full_local_path,
                           file_resolver.subentry(file_entry),
                           project_parameters,
                           path_mappings)


def diff_file_from_project(projects_folder: str,
                           args: ProgramArguments,
                           loaded_project_parameters: Optional[Dict[str, str]]) -> None:
    assert loaded_project_parameters

    if len(args.parameter) >= 2:
        project_name = args.parameter[0]
        file_to_edit = args.parameter[1]
    else:
        project_name = loaded_project_parameters["NAME"]
        file_to_edit = args.parameter[0]

    project_definition: ProjectDefinition = read_project_definition(projects_folder, project_name)
    path_mappings: Dict[str, str] = dict()
    process_folder(".", project_definition.file_resolver(), loaded_project_parameters, path_mappings)

    subprocess.call(["vimdiff", file_to_edit, path_mappings[file_to_edit]])

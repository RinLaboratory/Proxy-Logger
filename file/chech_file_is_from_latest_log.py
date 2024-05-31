from utils.types import TypesLoadedData


def CHECK_FILE_IS_FROM_LATEST_LOG(
    loaded_data: TypesLoadedData, file_lines: list[str], log_file: str
):
    for latest_file_data in loaded_data["latest_file"].values():
        file_lines_count = 0
        for latest_activity_data in loaded_data["latest_activity"][latest_file_data[2]]:
            if latest_activity_data in file_lines:
                file_lines_count += 1

        if len(loaded_data["latest_activity"][latest_file_data[2]]) == file_lines_count:
            print(
                "this file "
                + log_file
                + " includes a latest.log file that was previously loaded to the db. Marked latest.log for deletion."
            )
            return latest_file_data[2]
    return None

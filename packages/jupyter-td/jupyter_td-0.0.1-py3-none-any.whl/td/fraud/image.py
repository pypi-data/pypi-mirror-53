import os;
import sys;


def data_load_csv(csvPath, save_path, HbasePullPollSize = "8", ImageSavePoolSize="12" , TestTime="false"):
    ab_csv_path = os.path.abspath(csvPath);
    ab_save_path = os.path.abspath(save_path);
    if 0 < int(HbasePullPollSize) < 100:
        os.environ["HbasePullPollSize"] = HbasePullPollSize;
    else:
        os.environ["HbasePullPollSize"] = "20";

    if 0 < int(ImageSavePoolSize) < 100:
        os.environ["ImageSavePoolSize"] = ImageSavePoolSize;
    else:
        os.environ["ImageSavePoolSize"] = "20";

    os.environ["TestTime"] = str_to_bool_str(TestTime)

    if sys.version_info < (3, 0):
        commands = __import__("commands")
    else:
        commands = __import__("subprocess")
    (status, output) = commands.getstatusoutput(
        "java -jar /opt/jupyter/hbase/PullImages-1.0-SNAPSHOT.jar " + ab_save_path + " 2 " + ab_csv_path)
    if status == 0:
        print("download success!")
    else:
        print(output)


def str_to_bool_str(str):
    return "true" if str.lower() == 'true' else "false"
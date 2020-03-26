from First.SampleAll.InitFile import *
from First.SampleAll.Download import *
from First.SampleAll.Compression import *
from First.SampleAll.Sample_vxvault import sample_vxvault
from First.SampleAll.Sample_infosec import sample_infosec
from First.SampleAll.Sample_malshare import sample_malshare
from First.SampleAll.Sample_traffic import sample_traffic
from First.SampleAll.Sample_virusbay import sample_virusbay
from First.SampleAll.Sample_hybird import sample_hybird
from First.SampleAll.Sample_virussign import sample_virusign


def sample_archive():
    sample_dict = {
        # "https://www.hybrid-analysis.com": sample_hybird,
        # "http://www.virusign.com/get_hashlist.php": self.sample_virusign(),
        "http://www.malware-traffic-analysis.net": sample_traffic,# TODO many archive decompress
    }
    for website, info in sample_dict.items():
        information = f"START WEBSITE: {website}"
        write_log(information)
        result, detail = info()
        total_num = 0
        download_num = 0
        if result:
            for sample_md5, sample_detail in detail.items():
                total_num += 1
                sample_path = sample_detail["sample_path"]
                sample_url = sample_detail["sample_url"]
                option = sample_detail["option"] if "option" in sample_detail else {"timeout": 15}
                sessions = sample_detail["session"] if "session" in sample_detail else None
                download_result, information = download(sample_path, sample_url, sessions, **option)
                information = f"{sample_url} download result: {information}."
                if download_result:
                    download_num += 1
                    decompression_result, decompression_detail = decompression2folder(sample_path)
                    information = f"{information} decompression:{decompression_detail}."
                else:
                    write_md5(sample_md5)
                write_log(information)
        else:
            information = f"Failed: {detail}."
            write_log(information)
        information = f"END WEBSITE: {website}, total_num: {total_num}, download_num: {download_num}\n"
        write_log(information)


# TODO tans md5 to smartccl
def tans():
    pass


def sample_singer():
    sample_dict = {
        "https://malshare.com/api.php": sample_malshare,
        "http://vxvault.net/ViriList.php/ViriFiche.php": sample_vxvault,
        "https://beta.virusbay.io/sample/data": sample_virusbay,
        "https://infosec.cert-pa.it/analyze/": sample_infosec
    }
    for website, info in sample_dict.items():
        information = f"START WEBSITE: {website}"
        write_log(information)
        result, detail = info()
        total_num = 0
        download_num = 0
        if result:
            for sample_md5, sample_detail in detail.items():
                total_num += 1
                sample_path = sample_detail["sample_path"]
                sample_url = sample_detail["sample_url"]
                option = sample_detail["option"] if "option" in sample_detail else {"timeout": 15}
                download_result, information = download(sample_path, sample_url, **option)
                if download_result:
                    download_num += 1
                else:
                    write_md5(sample_md5)
                write_log(information)
        information = f"END WEBSITE: {website}, total_num: {total_num}, download_num: {download_num}\n"
        write_log(information)


# def run():
#     for website, info in sample_dict.items():
#         information = f"START WEBSITE: {website}"
#         write_log(information)
#         result, detail = info()
#         total_num = 0
#         download_num = 0
#         if result:
#             for sample_md5, sample_detail in detail.items():
#                 total_num += 1
#                 sample_path = sample_detail["sample_path"]
#                 sample_url = sample_detail["sample_url"]
#                 option = sample_detail["option"] if "option" in sample_detail else {"timeout": 15}
#                 download_result, information = download(sample_path, sample_url, **option)
#                 if download_result:
#                     download_num += 1
#                 else:
#                     write_md5(sample_md5)
#                 write_log(information)
#         information = f"END WEBSITE: {website}, total_num: {total_num}, download_num: {download_num}\n"
#         write_log(information)
# TODO tans sample to smartccl
# try:
#     compression_path = os.path.join(Init_dir, "[infected]" + download_date + ".rar")
#     compression(sample_dir, compression_path)
#     os.system(f"copy \"{compression_path}\" \"{smart_file_dir}\"")
#     write_log("-------ALL DONE--------")
# except Exception as e:
#     write_log(e)


if __name__ == "__main__":
    sample_archive()

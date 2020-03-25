from First.SampleAll.InitFile import *
from First.SampleAll.Download import *
from First.SampleAll.Sample_vxvault import sample_vxvault
from First.SampleAll.Sample_infosec import sample_infosec
from First.SampleAll.Sample_malshare import sample_malshare
from First.SampleAll.Sample_traffic import sample_traffic
from First.SampleAll.Sample_virusbay import sample_virusbay
from First.SampleAll.Sample_hybird import sample_hybird

sample_dict = {
    "http://vxvault.net/ViriList.php/ViriFiche.php": sample_vxvault,
    # "https://www.hybrid-analysis.com": sample_hybird,
    # "https://beta.virusbay.io/sample/data": sample_virusbay,
    # "https://malshare.com/api.php": sample_malshare,
    # "http://www.virusign.com/get_hashlist.php": self.sample_virusign(),
    # "http://www.malware-traffic-analysis.net": sample_traffic,
    "https://infosec.cert-pa.it/analyze/": sample_infosec
}


def run():
    for website, info in sample_dict.items():
        information = f"START WEBSITE: {website}"
        write_log(information)
        result, detail = info()
        if result:
            for sample_detail in detail.values():
                sample_path = sample_detail["sample_path"]
                sample_url = sample_detail["sample_url"]
                option = sample_detail["option"] if "option" in sample_detail else {"timeout": 15}
                download_result, information = download(sample_path, sample_url, **option)
                if download_result:
                    pass
                else:
                    write_log(information)
        else:
            information = f"END WEBSITE: {detail}\n"
            write_log(information)
    #     if type(sample_dict) is dict:
    #         if len(sample_dict) == 0:
    #             write_log(f"{website} today`s data is 0\n")
    #         else:
    #             for sample_md5, download_info in sample_dict.items():
    #                 result, info = download(download_info)
    #                 if result:
    #                     de_result, de_info = decompression_file(info)
    #                     write_log(de_info)
    #                 else:
    #                     write_log(info)
    #     else:
    #         write_log(f"{website} {sample_dict}\n")
    # try:
    #     compression_path = os.path.join(Init_dir, "[infected]" + download_date + ".rar")
    #     compression(sample_dir, compression_path)
    #     os.system(f"copy \"{compression_path}\" \"{smart_file_dir}\"")
    #     write_log("-------ALL DONE--------")
    # except Exception as e:
    #     write_log(e)


if __name__ == "__main__":
    run()

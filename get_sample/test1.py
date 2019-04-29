import requests





def get_session():
    user_agent = "Mozilla/5.0 (X11; Linux i686; rv:1.9.7.20) Gecko/2015-04-30 08:02:26 Firefox/3.8"
    headers = {"User-Agent": user_agent}
    session = requests.session()
    session.headers.update(headers)
    return session

def sample_hybird():
    user_data = {
        "User-Agent": "Falcon Sandbox",
        "api-key": "0ccgsgk0w00w4ogwcgk4o4s0ggw8gg4og04wsko8kw4s8wgocks400cgsg88400g"
    }
    session = get_session()
    session.headers.update(user_data)
    url = "https://www.hybrid-analysis.com/api/v2/feed/latest"
    try:
        sample_data = session.get(url).json()["data"]
        sample_sha256_list = [sample["sha256"] for sample in sample_data if sample["threat_level"] != 0]
        for sha256 in sample_sha256_list:
            sample_name = sha256 + ".vir.gz"
            sample_download_url = "https://www.hybrid-analysis.com/api/v2/overview/%s/sample" % sha256
        for sample in sample_data:
            if sample["threat_level"] != 0:
                sha256 = sample["sha256"]
                sample_name = sha256 + ".vir.gz"
                sample_download_url = "https://www.hybrid-analysis.com/api/v2/overview/%s/sample" % sha256
                print(sample_download_url)
                sample_sha256_list.append(sha256)

                # result = self.write_sample(sample_name, sample_download_url)
                # if result:
                #     print(result)
                #     self.success_num += 1
                # else:
                #     self.failed_num += 1
                    # self.write_failed_info(sha256)
        # write_download_log("www.hybrid-analysis.com")
    except:
        print(1)
        # write_download_log("(error: get JSON failed)" + "www.hybrid-analysis.com")
sample_hybird()
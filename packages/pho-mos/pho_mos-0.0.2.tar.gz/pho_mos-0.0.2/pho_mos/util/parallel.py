import concurrent.futures
import urllib.request as url_req
import os

from pho_mos.util import get_logger
LOGGER = get_logger("PARALLEL_UTIL")

def parallel_download(URLS: list,
                      result_path: str,
                      max_count: int = 1000,
                      image_prefix:str='img') -> bool:

    counter = 0
    # Retrieve a single page and report the URL and contents
    def load_url(img_link, timeout) -> bool:

        try:

            LOGGER.debug("Try download " + img_link)
            request_result = url_req.urlopen(img_link, timeout=timeout)
            raw_img = request_result.read()

            count_img_in_dir = len([i for i in os.listdir(result_path) if image_prefix in i]) + 1
            f = open(os.path.join(result_path, image_prefix + "_" + str(counter) + "." + 'jpeg'), 'wb')
            f.write(raw_img)
            f.close()
            LOGGER.debug("Success download")
            return True

        except Exception as e:
            LOGGER.debug("Could not load : " + str(img_link))
            LOGGER.debug(str(e))
            return False

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(URLS)) as executor:

        # Start the load operations and mark each future with its URL
        tasks = {executor.submit(load_url, url, 2): url for url in URLS}

        for future in concurrent.futures.as_completed(tasks):
            url = tasks[future]
            try:

                data = future.result()
                if data == True:
                    counter = counter + 1
                    if counter == max_count:
                        LOGGER.debug("Counter " + str(max_count) + " success download image")
                        executor.shutdown()
                        return True
            except Exception as exc:
                LOGGER.error('%r generated an exception: %s' % (url, exc))

        return True
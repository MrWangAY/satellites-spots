import math
import os
import urllib.request


def get_img(satellite_name, position, spot_alias, accuracy=4):
    base_url = "https://static.satbeams.com/tiles/"
    opener = urllib.request.build_opener()
    # 添加请求头
    opener.addheaders = {("Accept", "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"),
                         ("Accept-Encoding", "gzip,deflate,br"),
                         ("Accept-Language", "zh-CN,zh;q=0.9"),
                         ("Connection", "keep-alive"),
                         ("Cookie",
                          "__utmz=18407355.1650612990.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);_fbp=fb.1.1650614440851.668503034;__utmc=18407355;owa_v=cdh%3D%3E6d9d3f17%7C%7C%7Cvid%3D%3E1650613032050436634%7C%7C%7Cfsts%3D%3E1650613032%7C%7C%7Cdsfs%3D%3E3%7C%7C%7Cnps%3D%3E11;__gpi=UID=000004f81a41d624:T=1650613019:RT=1650873718:S=ALNI_MbTRZsrWhuCjLdEeypwsXjHxjSrIA;owa_s=cdh%3D%3E6d9d3f17%7C%7C%7Clast_req%3D%3E1650873723%7C%7C%7Csid%3D%3E1650873717250330289%7C%7C%7Cdsps%3D%3E1%7C%7C%7Creferer%3D%3E%28none%29%7C%7C%7Cmedium%3D%3Edirect%7C%7C%7Csource%3D%3E%28none%29%7C%7C%7Csearch_terms%3D%3E%28none%29;__gads=ID=54186bcd9231592b-229ac3456bd2003c:T=1650613036:RT=1650873724:S=ALNI_MaL6xXZXVILeBi2vJ3CcLNBi3pjxQ;__utma=18407355.1788090718.1650612990.1650789809.1650789809.14;__utmb=18407355.4.10.1650873716"),
                         ("Host", "static.satbeams.com"),
                         ("Referer", "https://satbeams.com/"),
                         ("Sec-Fetch-Dest", "image"),
                         ("Sec-Fetch-Mode", "no-cors"),
                         ("Sec-Fetch-Site", "same-site"),
                         ("User-Agent",
                          'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/100.0.4896.127Safari/537.36sec-ch-ua:"NotA;Brand";v="99","Chromium";v="100","GoogleChrome";v="100"'),
                         ("sec-ch-ua-mobile", "?0"),
                         ("sec-ch-ua-platform", "Windows")}
    urllib.request.install_opener(opener)
    # 构建文件夹（./image/位置/卫星名称）
    store_folder = './image_completed/' + str(position) + '/' + satellite_name + '/' + spot_alias
    # 获取瓦片的数量
    arr = math.pow(2, accuracy)
    if not os.path.exists(store_folder):
        os.makedirs(store_folder)
    for i in range(int(arr)):
        for j in range(int(arr)):
            # 依次在 i*j 方阵中寻找可以下载的波片
            url = base_url + spot_alias + '/' + str(accuracy) + '/' + str(i) + "/" + str(j) + ".png"
            filename = store_folder + '/' + str(accuracy) + '-' + str(i) + "-" + str(j) + ".png"
            print(url, filename)
            try:
                if os.path.exists(filename):
                    continue
                # 执行下载操作
                urllib.request.urlretrieve(url=url, filename=filename)
            except:
                print(url + " download false")


if __name__ == '__main__':

    position_folder = '../get_json_data/image_completed'
    # 获取位置信息
    positions = os.listdir(position_folder)
    positions = sorted(list(map(int, positions)))
    for position in positions:
        position = str(position)
        # 获取卫星名称
        for satellite in os.listdir(position_folder + "/" + position):
            # 获取波片别名
            for spot_alias in os.listdir(position_folder + "/" + position + '/' + satellite):
                # 获取图片
                image_folder = position_folder + "/" + position + "/" + satellite + '/' + spot_alias
                # 构建文件夹（./image/位置/卫星名称）
                store_folder = './integral_image/' + str(position) + '/' + satellite + '/'
                # 获取所有图像文件的列表
                image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.png')]
                # 计算每个小图像的大小和大图像的大小
                image_count = len(image_files)
                if image_count == 0:
                    print('Crawl image files not found in the directory ', image_folder)
                    get_img(satellite, position, spot_alias)






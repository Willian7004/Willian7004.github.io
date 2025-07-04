# Linux
本文介绍了我使用的Linux发行版以及配置局域网服务器的情况。

### 此前使用的Linux发行版

我尝试过不少Linux发行版，最终选择了Linux Mint，有几个方面的原因：
1. 在Ubuntu下游，N卡驱动、PPA以及Timeshift支持有优势。
2. Cinnamon桌面环境外观相对较好且接近Windows的操作习惯，对Xfce版本也进行了定制实现类似的外观且仍然适合低配设备。
3. 解决了Ubuntu过度依赖Snap的问题，仍然以系统包为主并引入Flatpak，并且能够自动换源。
4. 在apt换源和输入法安装的图形化支持较为完善。

Linux Mint也有一些缺点：
1. 软件不是最新，deb系这方面Debian Testing比较有优势，基本不需要使用Flatpak等方法安装比较新的软件。
2. 系统自带的smb服务器功能存在权限问题，如果需要开源smb服务器推荐iStoreOS或者NAS系统。
3. 默认外观不算优秀。由于外观较好的Solus Linux的主题实际上是使用了materia主题包和papirus图标包，可以用于其它不少发行版，在Linux Mint安装了这一主题，效果如下图。

<center class="half">
    <img src="https://github.com/Willian7004/new-blog/blob/main/files/dynamic/materia.jpg?raw=true" width="500"/>
</center>

基本配置和软件使用情况：
1. 浏览器用过Vivaldi，在低配设备流畅度高，同步功能比Firefox好用，但由于安卓版缺少扩展功能以及用不到j1800主机而换回了Edge。
3. 使用了Krita,LibreOffice和Inkscape等主流开源软件，游戏主要玩了画质相对较好的Openarena和SuperTuxKart。

### 近期使用的Linux发行版

考虑到有远程桌面需求，xrdp在手机基本不可用，kasmvnc画质差，pve的novnc等功能延时长，由于有用户反映Ubuntu24.04之后的远程桌面功能有较大优势，就改用最新的Ubuntu25.04。

根据一些文章判断，Ubuntu的远程桌面表现提升是因为用了性能更好的Wayland、远程桌面功能与系统集成以及在Gnome桌面对远程桌面需要的分辨率和画质调整做了优化。实际使用时在设置中有“远程桌面”和“远程登录”功能，前者与物理机共用会话但需要使用相同分辨率，在手机使用Windows APP连接无法修改宽高比，改用后一种方案，该方案与xrdp类似，都需要注销后切换远程连接和物理机。实际流畅度表现比xrdp好很多但比Windows的rdp差一些。另外，在远程桌面时不支持手机输入法也无法启动电脑上的输入法，导致无法输入中文。

除rdp功能外Ubuntu25.04相比Linux Mint的优点包括：
1. 自动换源且预装输入法。
2. 流畅度较高。
3. 内核和软件版本新。
缺点包括：
1. 没有轮播壁纸。
2. 文件管理器频繁闪退。
3. 不同应用外观不太一致。
4. 缺乏对盒盖操作等功能的图形化设置项。

### 局域网服务器配置

##### 其它方案的缺陷：
1. iStoreOS较为轻量化且服务部署方便，但我有使用桌面系统的需求，iStoreOS内核有裁剪，通过Docker部署带KASM VNC的桌面系统不能正常使用部分功能。
2. PVE方便使用和测试多个系统，但ip地址改变时难以修复，显卡直通依赖额外配置。
3. 在iStoreOS可以部署PVE，能解决ip地址问题，但也存在虚拟机无法与iStoreOS使用同一个硬盘，连接smb有功能限制的问题。

##### ssh与文件服务器

远程终端控制安装ssh即可，有需要时需要允许root登录。由于在安卓设备连接基本不可用，后面改回物理机使用。

文件服务器由于smb不能正常使用，还是决定使用sftp。在安卓可以通过Solid Explorer等客户端连接。在Windows需要安装WinFSP和sshfs-win再映射网络驱动器，路径使用“\sshfs.r\用户名@IP地址!端口号\home”实现按绝对路径挂载。

##### Docker应用

使用Docker部署局域网服务，有以下优点：
1. 安装流程简单，没有依赖问题。
2. 无需额外配置就能解决第三方服务的局域网访问问题。
3. 方便进行容器启停和版本管理等操作。

不过Docker也有一些缺点：
1. 缺乏稳定的镜像站。
2. 集成依赖性和多版本管理对容量占用大。
3. 需要额外的工具链进行具体监测。

目前部署的应用包括：

**1.Streamlit：**

指令：
```bash
docker run -d -p 8501:8501 -v /home/william/github/new-blog:/program --name new-blog --restart unless-stopped python:3.12-slim /bin/bash -c "apt update && apt-get install -y git && pip install streamlit gitpython -i https://mirrors.aliyun.com/pypi/simple/ && cd /program && streamlit run streamlit_app.py --server.port 8501"
```

**2.dpanel，用于图形化Docker管理：**

指令：
```bash
docker run -d --name dpanel --restart=always \
 -p 8807:8080 -e APP_NAME=dpanel \
 -v /var/run/docker.sock:/var/run/docker.sock \
 -v /home/dpanel:/dpanel dpanel/dpanel:lite
```

**3.Jellyfin,用于以图片/视频为主的媒体库：**

docker-compose.yml:
```yaml
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    network_mode: 'host'
    restart: 'unless-stopped'
    volumes:
      - /var/lib/docker/volumes/jellyfin-config/_data:/config
      - /var/lib/docker/volumes/jellyfin-cache/_data:/cache
      - type: bind
        source: /mnt/sda/Documents
        target: /media
```
指令：
`sudo docker compose -p jellyfin-server up`\
创建docker卷：
`docker volume create jellyfin-config`\
删除docker卷：
`docker volume rm jellyfin-config`

**4.Komga，用于文档媒体库**

docker-compose.yml:
```yaml
version: '3.3'
services:
  komga:
    image: gotson/komga
    container_name: komga
    volumes:
      - type: bind
        source: /var/lib/docker/volumes/komga-config
        target: /config
      - type: bind
        source: /mnt/sda/Documents
        target: /data
    ports:
      - 25600:25600
    user: "1000:1000"
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
```
指令：\
（首次启动）`sudo chmod 777 -R /var/lib/docker/volumes/komga-config`\
`sudo docker compose -p komga up`

**5.Watchtowver，用于自动更新Docker镜像：**
```bash
docker run -d \
    --name watchtower --restart unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    containrrr/watchtower --cleanup
```

**6.OpenWebUI，用于LLM对话，搜索和代码执行功能有优势：**
```bash
docker run -d -p 3000:8080 \
--add-host=host.docker.internal:host-gateway \
-v open-webui:/app/backend/data \
--name open-webui --restart unless-stopped \
ghcr.io/open-webui/open-webui:main
```

##### 下载服务器

由于百度网盘Linux版没有p2p加速且wine版本不能正常运行，阿里云盘官方速度只略高于1mb/s且第三方客户端更慢，目前不在Linux使用网盘客户端。

使用图形界面时，通过Xtreme Download Manager进行下载，能实现资源嗅探和多线程下载等功能。

由于前面提到的安卓连接xrdp延时过长的问题，需要通过终端进行远程连接，目前会用到以下两个下载应用：

**1.hfd，由hf-mirror开发，用于下载AI模型和数据集：**

获取：
```bash
wget https://hf-mirror.com/hfd/hfd.sh
chmod a+x hfd.sh
```
设置环境变量（每次打开终端）：
```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_TOKEN=
```
下载模型：
```bash
cd /mnt/sda/Documents/Download/hfd
./hfd.sh gpt2
```
下载数据集：
```bash
cd /mnt/sda/Documents/Download/hfd
./hfd.sh wikitext --dataset
```
匹配文件名:\
1.指定格式，`-r`为递归：`--include -r *.json`\
2.排除文件：`--exclude readme.md`\
3.文件范围：`--include model-0000[1-4]-of-00004.safetensors`

**2.aria2，用于下载链接：**

前台下载（关闭终端会终止下载）：\
`aria2c https://hf-mirror.com/deepseek-ai/DeepSeek-V3-0324/resolve/main/README.md?download=true`\
后台下载：\
`nohub aria2c https://hf-mirror.com/deepseek-ai/DeepSeek-V3-0324/resolve/main/README.md?download=true`\
查看后台任务（仅在当前SSH有效）：`jobs -l`\
全局检查进程：`ps aux | grep aria2c`

### 未采用的软件

我了解过其它一些Linux优化措施和软件，但因为一些原因没有采用。

##### 透明终端与终端应用美化

透明终端是比较常见的美化方案，但我个人更注重开箱即用，就没有进行这类配置。目前Kali Linux在有Kali主题的桌面环境中也是透明终端。

终端应用讨论比较多的是Vim，常见的美化方法是添加路径显示和分屏实现类似于IDE的功能，也可以进行定制对其它用途进行优化。

##### 云原生软件

目前大部分工具类应用是桌面应用而非web应用，但不少类型的应用有web版本。比如用于文档编辑的OnlyOffice，用于代码编辑的CodeServer和用于协作的NextCloud。

我没有部署这类应用的原因如下：
1. 相比集中存储，考虑外出使用等情况，我更注重各设备的单独运行效果。
2. 通过挂载网络存储器，可以实现在本地编辑服务器上的内容。

##### 集群管理

docker swarm和k8s分别能满足小集群和大集群的容器管理需求。我部署应用由于是个人使用，对高可用要求不高，并且没有多版本和多设备需求，因此没有使用这类应用。

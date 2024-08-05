PC側
source ~/work/yolov8/bin/activate
python ~/ros2_ws/src/raspimouse_drone_ros2/controller.py

ラズパイマウス側
~/RaspberryPiMouse/utils/build_install.bash
ros2 launch raspimouse raspimouse.launch.py
ros2 run raspimouse_drone_ros2 receiver

新規PCインストール
https://zenn.dev/pon_pokapoka/articles/nvidia_cuda_install
https://qiita.com/tf63/items/0c6da72fe749319423b4
https://qiita.com/Hiro23/items/096cb312f5c2944a27d5

・usbメモリをFATでフォーマット
容量6GB以上
・Ubuntu 22.04 LTSイメージのダウンロード
https://releases.ubuntu.com/jammy/
ubuntu-22.04.4-desktop-amd64.iso
・blenaEtcherでイメージをusbメモリに書き込み
・PCのbiosを立ち上げる
F2キーなど
https://www2.mouse-jp.co.jp/ssl/user_support2/sc_faq_documents.asp?FaqID=36044&_ga=2.234435804.337368445.1715033280-144711906.1688346585
・usbメモリから起動してubuntuをインストール
・フォルダ名の英語化
https://demura.net/misc/21950.html
$ LANG=C xdg-user-dirs-gtk-update
・nvidia-driverインストール -> cudaインストール -> cuDnnインストール
色々なやり方がサイトに記載されているが、バージョンの指定が難しい
最近は自動的にバージョンを選ぶ方法が出てきているらしい
https://zenn.dev/pon_pokapoka/articles/nvidia_cuda_installが参考になる
・nvidia-driverインストール
ubuntu-drivers devicesでハードウェアに対応したNVIDIAドライバを探す
Nvidia-driver-555がrecomendedされたが途中でうまくいかなかった。
結局はNvidia-driver-550となった。
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install nvidia-driver-550
・nvidia-driverインストールはデフォルトでロードされている [nouveau] ドライバーを無効化しないとできなかった。
# lsmod | grep nouveau
# vi /etc/modprobe.d/blacklist-nouveau.conf
# 最終行に追記 (ファイルがない場合は新規作成)
blacklist nouveau
options nouveau modeset=0
# update-initramfs -u
# reboot
・インストール確認用のコマンドnvidia-smiで成功を確認する
・CUDAのインストール
CUDA Toolkit Archive から deb (network) を選択してインストール用コマンドを取得
https://developer.nvidia.com/cuda-downloads
Linux -> x86_64 -> Ubuntu -> 22.04 -> deb(network)
これをやったが、失敗している。
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-6
こっちで自動でバージョンを探した方がいいかも
sudo apt install cuda-toolkit
結局はcuda-toolkit-12-4が入った
・nvcc-VでCUDAの確認
・cuDNNのインストール
cuDNN Archiveからインストールするパッケージを選択 (NVIDIAアカウントの登録が必要）
https://developer.nvidia.com/rdp/cudnn-archive
選択してインストールしようとしたがパッケージがないと言われる。
Download cuDNN v8.9.7 (December 5th, 2023), for CUDA 12.x
結局はsudo apt install cudnn9で自動的にバージョンを選択してインストールした
その結果、cuDnn9.3.0が入ったぽい。CUDA12.6用になっていてCUDA12.4と合っていないが動いている。
・今後、sudo apt update; sudo apt upgradeで勝手にnvidia-driver、cuda、 cuDnnがバージョンアップされるらしい（その時動かなくなるかも）。sudo apt-mark hold nvidia-driver-550で自動更新をストップできるらしいがやってない。
・GPUが使えるか確認
pip3 install torch
Pythonを立ち上げて以下のコマンドでtrueが出る
torch.cuda.is_available()
・yolov8をインストール
pip install ultralytics
yolo predict model=yolov8n.pt source=0
・ROS2 humbleインストール

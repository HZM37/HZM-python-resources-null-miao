import os
import shutil
import customtkinter as ctk
import threading  #引入多线程，房卡死

#1.设计外观
ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')
ctk.set_widget_scaling(1.2)   #整体放大适配2k

#2.创建主窗口
app = ctk.CTk()
app.title('一键整理文件神器-null_喵')
app.geometry('650x400')

def mimi():
    target_path = entry_path.get()
    if not target_path or not os.path.exists(target_path):
        label_tip.configure(text='路径不存在，请检查后输入！',text_color='red')
        return

    label_tip.configure(text='正在疯狂整理中，请稍后...',text_color='green')
    btn_start.configure(state='disabled')

    def nini():
        try:
            pic_dir = os.path.join(target_path, '图片')
            doc_dir = os.path.join(target_path, '文档')
            zip_dir = os.path.join(target_path, '压缩包')
            mp4_dir = os.path.join(target_path, '视频')
            qit_dir = os.path.join(target_path, '其他')

            for b in [pic_dir,doc_dir,zip_dir,mp4_dir,qit_dir]:
                if not os.path.exists(b):
                    os.mkdir(b)

            files = os.listdir(target_path)
            for file in files:
                file_path = os.path.join(target_path, file)
                if os.path.isdir(file_path):
                    continue
                if file.startswith('.'):
                    continue

                if file.endswith(('.jpg','.jpeg','.png','.gif','bmp','.webp','.svg')):
                    shutil.move(file_path, os.path.join(pic_dir, file))
                elif file.endswith(('.txt','.pdf','.docx','.doc','.xisx','.xis','.pptx','.csv')):
                    shutil.move(file_path, os.path.join(doc_dir, file))
                elif file.endswith(('.7z','.rar','.bz2','.zip','.gz','.xz')):
                    shutil.move(file_path, os.path.join(zip_dir, file))
                elif file.endswith(('.mp4','.mkv','.avi','.mov','.wmv')):
                    shutil.move(file_path, os.path.join(mp4_dir, file))
                else:
                    shutil.move(file_path, os.path.join(qit_dir, file))

            label_tip.configure(text='整理完成！强迫症表示极度舒适。',text_color='green')
        except Exception as e:
            label_tip.configure(text=f'出错了：{e}', text_color='red')
        finally:
            btn_start.configure(state='normal')

    threading.Thread(target=nini).start()

#4.ui界面
label_title = ctk.CTkLabel(app, text=" 请输入你要整理的文件夹绝对路径：", font=("微软雅黑", 18, "bold"))
label_title.pack(pady=(30, 10))

entry_path = ctk.CTkEntry(app, width=480, height=40, placeholder_text="例如：C:/Users/xxx/Desktop/测试")
entry_path.pack(pady=10)

btn_start = ctk.CTkButton(app, text="开始一键整理", width=220, height=45, font=("微软雅黑", 16, "bold"), command=mimi)
btn_start.pack(pady=20)

label_tip = ctk.CTkLabel(app, text="准备就绪，等待指令。", font=("微软雅黑", 14))
label_tip.pack(pady=10)

# 5. 让窗口一直运行
app.mainloop()
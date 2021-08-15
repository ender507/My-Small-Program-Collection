from PIL import Image


if __name__ == '__main__':
    pic_id = (57, 557)
    frame_num = (121, 111)
    for i in range(2):
        imgs = []
        for j in range(frame_num[i]+1):
            pic_name = str(pic_id[i]) + '_frames\\' + str(pic_id[i]) + '_' + str(j) +'.png'
            pic = Image.open(pic_name)
            if imgs == []:
                imgs.append(pic)
                size = pic.size
            else:
                tmp = Image.new("RGB", size, "#000000")
                tmp.paste(pic)
                imgs.append(tmp)
        imgs[0].save(str(pic_id[i]) + '.gif', save_all=True,
                     append_images=imgs, duration=0.2,transparency=255)


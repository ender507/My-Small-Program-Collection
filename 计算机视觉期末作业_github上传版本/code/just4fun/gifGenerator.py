from PIL import Image


if __name__ == '__main__':
    frame_num = 171
    imgs = []
    for j in range(frame_num+1):
        pic_name = 'gif\\1_' + str(j) +'.png'
        pic = Image.open(pic_name)
        if imgs == []:
            imgs.append(pic)
            size = pic.size
        else:
            tmp = Image.new("RGB", size, "#000000")
            tmp.paste(pic)
            imgs.append(tmp)
    imgs[0].save('1.gif', save_all=True,
                append_images=imgs, duration=0.2,transparency=255)


from PIL import Image
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tqdm import tqdm

def differences(pixel_a, pixel_b):
    return list([abs(a-b) for a, b in zip(pixel_a, pixel_b)])


def add_diffs(img, xy_a, xy_b, diff_counts):
    x_a, y_a = xy_a
    x_b, y_b = xy_b

    diff_counts_a = diff_counts[y_a][x_a]
    diff_counts_b = diff_counts[y_b][x_b]

    a_layers = get_layers(img.getpixel(xy_a))
    b_layers = get_layers(img.getpixel(xy_b))

    for layer_index, (a, b) in enumerate(zip(a_layers, b_layers)):
        diff = abs(a-b)
        diff_counts_a[layer_index] += diff
        diff_counts_b[layer_index] += diff


def get_layers(pixel):
    if type(pixel) is int:
        return (pixel,)
    return pixel


def set_layers(layers):
    if len(layers) == 0:
        return layers[0]
    return layers


def main():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

    
    exts = Image.registered_extensions()
    supported_extensions = [(f,ex) for ex, f in exts.items() if f in Image.OPEN]
    supported_extensions = [('All Files','*.*')] + sorted(list(supported_extensions), key=lambda a: a[0])
    
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    original = Image.open(filename)
##    print(f'{original.getpixel((0,0))=}')
    layer_count = len(get_layers(original.getpixel((0,0))))
    width, height = original.size

    diff_counts = [[[0]*layer_count for pixel in range(width)] for row in range(height)]

    pbar_count = 0
    actual_count = 0
    with tqdm(total=height*width) as pbar:
        for y in range(height):
            for x in range(width):
                has_below = y + 1 < height
                has_right = x + 1 < width

                this_color = get_layers(original.getpixel((x, y)))
                this_diff_counts = diff_counts[y][x]

                if has_below:
                    add_diffs(original, (x,y), (x,y+1), diff_counts)

                if has_right:
                    add_diffs(original, (x,y), (x+1,y), diff_counts)

                if has_below and has_right:
                    add_diffs(original, (x,y), (x+1,y+1), diff_counts)
                    
                actual_count += 1
                if actual_count - pbar_count > height*width/10 or actual_count == height*width:
                    pbar.update(actual_count - pbar_count)
                    pbar_count = actual_count

    # 'P' mode in PIL.Image is 0-255 grayscale
    diffed = Image.new(original.mode, original.size)
    diffed.palette = original.palette

    for y in range(height):
        for x in range(width):
            # TODO it might not always be 255. Check the mode for layer bit depth
            diffed_color = tuple(min(255, layer_diff) for layer_diff in diff_counts[y][x])
            diffed.putpixel((x, y), set_layers(diffed_color))
##    print(f'{diffed.mode=}')

    diffed.show(title='Difference Map')
    should_save = None
    while should_save is None:
        answer = input('Save? [Y/n] ')
        answer_clean = answer.lower().strip()
        if answer in ['y', 'yes']:
            should_save = True
        elif answer in ['n', 'no']:
            should_save = False
        else:
            print('Invalid selection:', repr(answer))
            print()

    if should_save:
        exts = Image.registered_extensions()
        supported_extensions = [(f,ex) for ex, f in exts.items() if f in Image.SAVE]
        supported_extensions = [('All Files','*.*')] + sorted(list(supported_extensions), key=lambda a: a[0])
##        print('\n'.join(repr(i) for i in supported_extensions))
        filename = ''
        while filename == '':
            print(f'{supported_extensions=}')
            filename = asksaveasfilename(filetypes=supported_extensions,defaultextension='.png')
            print(f'{filename=}')
            if filename == '':
                print('Save cancelled. Press Enter to finish, or type \'Save\' to try again.')
                answer = input()
                if answer == '':
                    exit(0)

        diffed.save(filename)


if __name__ == '__main__':
    main()

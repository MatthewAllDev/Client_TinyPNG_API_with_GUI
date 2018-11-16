# Module for GUI for TinyPNG API with keys balanced functions
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru> <GitHub @MatthewAllDev>
# version 1.0 beta dated November 16, 2018

import fnmatch
import os
from sys import maxsize

import tinify

import MainGUI as Gui


def validate_key(key):
    api = tinify.tinify
    try:
        api.key = key
        api.validate()
        return True
    except tinify.Error:
        return False


def start_compressing(master, input_directory, method=None, height=None, width=None):
    if not len(master.settings.keys):
        Gui.Window.error_message('none_keys')
        master.init_settings_window()
        return
    files = os.listdir(input_directory)
    images = fnmatch.filter(files, "*.jpg")
    images.extend(fnmatch.filter(files, "*.png"))
    output_directory = os.path.join(input_directory, 'Processed')
    try:
        os.makedirs(output_directory)
    except FileExistsError:
        files_processed = os.listdir(output_directory)
        images_processed = fnmatch.filter(files_processed, "*.jpg")
        images_processed.extend(fnmatch.filter(files_processed, "*.png"))
        for i in range(0, len(images_processed)):
            try:
                images.remove(images_processed[i])
            except ValueError:
                continue
    if len(images):
        window = master.init_action_process_window()
        settings = master.settings
        window.ProgressBar['maximum'] = len(images)
        window.ProgressBar.update()
        result = 'Complete!'
        if method:
            window.titleText.set('Resize and compressing...')
            window.OkButton.config(command=window.parent.init_resize_and_compressing_window)
            for image in images:
                if not window.stop_process_flag:
                    result = resize_image_and_compressing(window, settings, image, input_directory, output_directory,
                                                          method, height, width)
                    if result == 'Error!':
                        break
                else:
                    result = 'Stopped!'
                    break
        else:
            window.titleText.set('Compressing...')
            window.OkButton.config(command=window.parent.init_compressing_window)
            for image in images:
                if not window.stop_process_flag:
                    result = compressing_image(window, settings, image, input_directory, output_directory)
                    if result == 'Error!':
                        break
                else:
                    result = 'Stopped!'
                    break
        window.OkButton.config(state='normal')
        window.StopButton.config(state='disable')
        window.titleText.set(result)
        settings.save_settings()
    else:
        Gui.Window.error_message('need_files_to_processing')


def resize_image_and_compressing(window, settings, image, input_directory, output_directory, method, height, width):
    window.ProgressText.set('%s (%d/%d)' % (image, window.ProgressBar['value'] + 1, window.ProgressBar['maximum']))
    window.ProgressBar.update()
    api = tinify.tinify
    api.key = change_api_key(settings.keys)
    method = method.lower()
    try:
        source = api.from_file(os.path.join(input_directory, image))
        if height and not width:
            height = int(height)
            modified_image = source.resize(method=method, height=height)
        elif width and not height:
            width = int(width)
            modified_image = source.resize(method=method, width=width)
        else:
            height = int(height)
            width = int(width)
            modified_image = source.resize(method=method, height=height, width=width)
        modified_image.to_file(os.path.join(output_directory, image))
        settings.keys[api.key] = api.compression_count
        window.ProgressBar['value'] += 1
        window.ProgressBar.update()
    except tinify.AccountError:
        settings.keys[api.key] = api.compression_count
        if len(settings.keys):
            resize_image_and_compressing(window, settings, image, input_directory, output_directory, method, height,
                                         width)
        else:
            Gui.Window.error_message('api_key_constraint_error', api.compression_count)
            return 'Error!'
    except tinify.ClientError as e:
        Gui.Window.error_message('api_client_error', e)
        return 'Error!'
    except tinify.ServerError:
        Gui.Window.error_message('api_server_error')
        return 'Error!'
    except tinify.ConnectionError:
        Gui.Window.error_message('network_connection_error')
        return 'Error!'


def compressing_image(window, settings, image, input_directory, output_directory):
    window.ProgressText.set('%s (%d/%d)' % (image, window.ProgressBar['value'] + 1, window.ProgressBar['maximum']))
    window.ProgressBar.update()
    api = tinify.tinify
    api.key = change_api_key(settings.keys)
    try:
        source = api.from_file(os.path.join(input_directory, image))
        source.to_file(os.path.join(output_directory, image))
        settings.keys[api.key] = api.compression_count
        window.ProgressBar['value'] += 1
        window.ProgressBar.update()
    except tinify.AccountError:
        settings.keys[api.key] = api.compression_count
        if len(settings.keys):
            compressing_image(window, settings, image, input_directory, output_directory)
        else:
            Gui.Window.error_message('api_key_constraint_error', api.compression_count)
            return 'Error!'
    except tinify.ClientError as e:
        Gui.Window.error_message('api_client_error', e)
        return 'Error!'
    except tinify.ServerError:
        Gui.Window.error_message('api_server_error')
        return 'Error!'
    except tinify.ConnectionError:
        Gui.Window.error_message('network_connection_error')
        return 'Error!'


def change_api_key(keys):
    min_compression_count = maxsize
    result_key = None
    for key in keys:
        if keys[key] == '':
            return key
        elif keys[key] < min_compression_count:
            result_key = key
            min_compression_count = keys[key]
    return result_key

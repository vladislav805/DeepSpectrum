[![Coverage Status](https://coveralls.io/repos/github/DeepSpectrum/DeepSpectrum/badge.svg)](https://coveralls.io/github/DeepSpectrum/DeepSpectrum)
[![Build Status](https://travis-ci.org/DeepSpectrum/DeepSpectrum.svg?branch=master)](https://travis-ci.org/DeepSpectrum/DeepSpectrum)
[![Anaconda-Server Badge](https://anaconda.org/deepspectrum/deepspectrum/badges/version.svg)](https://anaconda.org/deepspectrum/deepspectrum)
[![Anaconda-Server Badge](https://anaconda.org/deepspectrum/deepspectrum/badges/platforms.svg)](https://anaconda.org/deepspectrum/deepspectrum)
[![Anaconda-Server Badge](https://anaconda.org/deepspectrum/deepspectrum/badges/installer/conda.svg)](https://conda.anaconda.org/deepspectrum)


**DeepSpectrum** is a Python toolkit for feature extraction from audio data with pre-trained Image Convolutional Neural Networks (CNNs). It features an extraction pipeline which first creates visual representations for audio data - plots of spectrograms or chromagrams - and then feeds them to a pre-trained Image CNN. Activations of a specific layer then form the final feature vectors.

**(c) 2017-2020 Shahin Amiriparian, Maurice Gerczuk, Sandra Ottl, Björn Schuller: Universität Augsburg**
Published under GPLv3, see the LICENSE.md file for details.

Please direct any questions or requests to Shahin Amiriparian (shahin.amiriparian at tum.de) or Maurice Gercuk (maurice.gerczuk at informatik.uni-augsburg.de).

# Citing
If you use DeepSpectrum or any code from DeepSpectrum in your research work, you are kindly asked to acknowledge the use of DeepSpectrum in your publications.
> S. Amiriparian, M. Gerczuk, S. Ottl, N. Cummins, M. Freitag, S. Pugachevskiy, A. Baird and B. Schuller. Snore Sound Classification using Image-Based Deep Spectrum Features. In Proceedings of INTERSPEECH (Vol. 17, pp. 2017-434)


# Installation
The easiest way to install DeepSpectrum is through the packages on our official conda channel which will be built for every release tag on the master branch. For installing different branches or a more manual approach, you can also use the setup.py script with [pip](#installation-through-pip) (only for Linux) and also an environment.yml for installing through [conda](#conda-installation) (recommended on Windows and OSX). For manual installation you also have to pull in the auDeep submodule:
```bash
git submodule update --init --recursive
```



## Dependencies (only for installation with pip)
* Python >=3.6
* ffmpeg

## Installing the conda packages
First, you have to add the pytorch and conda-forge channels to your conda channel configuration:
```bash
conda config --add channels pytorch
conda config --add channels conda-forge
```

Then you can install DeepSpectrum into a new environment:
```bash
conda create -n DeepSpectrum -c deepspectrum deepspectrum
```

Finally, activate your DeepSpectrum environment and start using the tool:
```bash
conda activate DeepSpectrum
```
Installation is now completed - you can skip to [configuration](#configuration) or [usage](#using-the-tool).


## Manual Conda installation
You can use the included environment.yml file to create a new virtual python environment with DeepSpectrum by running:
```bash
conda env create -f environment.yml
```
Then activate the environmnet with:
```bash
conda activate DeepSpectrum
```

Installation is now completed - you can skip to [configuration](#configuration) or [usage](#using-the-tool).


## Installation through pip (for Linux)
We recommend that you install the DeepSpectrum tool into a virtual environment. To do so first create a new virtualenvironment:
```bash
virtualenv -p python3 ds_virtualenv
```
If you have a recent installation of tensorflow (>=1.12) on your system, you can also create a virtualenvironment that incorporates you system python packages:
```bash
virtualenv -p python3 --system-site-packages ds_virtualenv
```
This creates a minimal python installation in the folder "ds_virtualenv". You can choose a different name instead of "ds_virtualenv" if you like, but the guide assumes this name.
You can then activate the virtualenv (Linux):
```bash
source ds_virtualenv/bin/activate
```

Once the virtualenv is activated, the tool can be installed from the source directory (containing setup.py) with this command:
```bash
pip install .
```

Installation is now completed - you can skip to [configuration](#configuration) or [usage](#using-the-tool).

## Manually updating auDeep
We try to keep the auDeep submodule up to date, e.g. when new parsers are added. For the case that the submodule lags behind the latest commit in the auDeep main repository and you encounter issues, like `ModuleNotFoundError: No module named 'audeep.backend.parsers.[parser_module]'`, you can manually update auDeep (activate your virtual python environment first):
```bash
git submodule foreach git pull origin master
pip install ./auDeep/
```


## Configuration
If you just want to start working with ImageNet pretrained keras-application models, skip to [usage](#using-the-tool). Otherwise, you can adjust your configuration file to use other weights for the supported models. The default file can be found in `deep-spectrum/src/cli/deep.conf`:
```
[main]
size = 227
backend = keras

[keras-nets]
vgg16 = imagenet
vgg19 = imagenet
resnet50 = imagenet
inception_resnet_v2 = imagenet
xception = imagenet
densenet121 = imagenet
densenet169 = imagenet
densenet201 = imagenet
mobilenet= imagenet
mobilenet_v2 = imagenet
nasnet_large = imagenet
nasnet_mobile = imagenet

[pytorch-nets]
alexnet=
squeezenet=
googlenet=

```
Under `keras-nets` you can define network weights for the supported models. Setting the weights for a model to `imagenet` is the default and uses ImageNet pretrained models from `keras-aplications`. Three additional networks are also supported through pytorch: `alexnet`, `squeezenet` and `googlenet`. For these, no definition of the used weights is needed (or possible, for the time being). The downloaded `keras-nets` will be stored in `$HOME/.keras`.

# Using the tool
You can access the scripts provided by the tool from the virtualenvironment by calling `deepspectrum`. The feature extraction component is provided by the subcommand `features`.
> Вы можете получить доступ к скриптам, предоставляемым инструментом, из virtualenv, вызвав `deepspectrum`. Компонент извлечения функций предоставляется подкомандой `features`.

## Features for AVEC2018 CES
The command below extracts features from overlapping 1 second windows spaced with a hop size of 0.1 seconds (`-t 1 0.1`) of the the file `Train_DE_01.wav`. It plots mel spectrograms (`-m mel`) and feeds them to a pre-trained VGG16 model (`-en vgg16`). The activations on the fc2 layer (`-fl fc2`) are finally written to `Train_DE_01.arff` as feature vectors in arff format. `-nl` suppresses writing any labels to the output file. The first argument after `deepspectrum features` must be the path to the audiofile(s).
> Приведенная ниже команда извлекает объекты из перекрывающихся 1-секундных окон с интервалом в 0.1 секунды (`-t 1 0.1`) файла `Train_DE_01.wav`. Он строит спектрограммы mel (`-m mel`) и передает их на предварительно обученную модель VGG16 (` -en vgg16`). Активации на слое fc2 (`-fl fc2`) наконец записываются в `Train_DE_01.arff` как векторы объектов в формате arff.  `-nl` подавляет запись любых меток в выходной файл. Первым аргументом после `deepspectrum features` должен быть путь к аудиофайлу (файлам).
```bash
deepspectrum features Train_DE_01.wav -t 1 0.1 -nl -en vgg16 -fl fc2 -m mel -o Train_DE_01.arff
```

## Commandline Options
All options can also be displayed using `deepspectrum features --help`.
> Все параметры также могут быть отображены с помощью `deepspectrum features --help`.
### Required options
| Option   | Description | Default |
|----------|-------------|---------|
| -o, --output | Расположение выходного файла объектов. Поддерживаемые форматы вывода: файлы значений, разделенные запятыми, и файлы arff. Если расширение указанного выходного файла *.arff*, в качестве формата выбирается arff, в противном случае вывод будет в формате значений, разделенных запятыми. | None |


### Извлечение признаков из аудио фрагментов
| Option   | Description | Default |
|----------|-------------|---------|
| -t, --window-size-and-hop | Определить окно и hopsize для извлечения признаков. E.g `-t 1 0.5` извлекает признаки из 1-секундных фрагментов каждые 0.5 секунды. | Извлечение из всего аудио файла. |
| -s, --start | Установите время начала (в секундах), из которого признаки должны быть извлечены из аудиофайлов. | 0 |
| -e, --end | Установите время окончания, до которого признаки должны быть извлечены из аудиофайлов. | None |

### Настройка параметров для звуковых графиков
| Option   | Description | Default |
|----------|-------------|---------|
| `-m`, `--mode` | Тип графика для использования в системе (Выбор из: 'spectrogram', 'mel', 'chroma'). | spectrogram |
| `-fs`, `--frequency-scale` | Масштаб для оси Y графиков, используемых системой (Выбор из: 'linear', 'log' и 'mel'). Игнорируется, если mode=chroma или mode=mel. (default: `linear`)
| `-fql`, `--frequency-limit` | Предел для оси Y на графике спектрограммы по частоте. | None |
| `-d`, `--delta` | Если указано, производные данного порядка выбранных объектов отображаются на графиках, используемых системой. | None |
| `-nm`, `--number-of-melbands` | Количество melbands, используемыых для вычисления melspectrogram. Действует только с mode=mel. | 128 |
| `-nfft` | Длина FFT window, используемая для создания спектрограммы в количестве образцов. Рассмотрите возможность выбора меньших значений при извлечении из небольших сегментов. | Следующая степень двойки от 0.025 x sampling_rate_of_wav |
| `-cm`, `--colour-map` | Цветовая карта matplotlib для создания графиков спектрограмм. | `viridis` |

### Параметры для извлечения признаков CNN
| Option   | Description | Default |
|----------|-------------|---------|
| `-en`, `--extraction-network` | Выберите сеть для извлечения признаков, как указано в файле конфигурации | `alexnet` |
| `-fl`, `--feature-layer` | Название слоя, из которого должны быть извлечены признаки. | `fc2` |

### Определение информации метки
You can use csv files for label information or explicitly set a fixed label for all input files. If you use csv files, numerical features are supported (e.g. for regression). If you do neither of those, each file is assigned the name of its parent directory as label. This can be useful if your folder structure already represents the class labels, e.g.
> Вы можете использовать CSV-файлы для метки информации или явно установить фиксированную метку для всех входных файлов. Если вы используете CSV-файлы, поддерживаются числовые признаки (например, для регрессии). Если вы не делаете ни того, ни другого, каждому файлу будет присвоено имя его родительского каталога в качестве метки. Это может быть полезно, если ваша структура директорий уже представляет метки классов, например:
```
data                          Base Directory of your data
  ├─── class0                 Directory containing members of 'class0'
  |    └─── instance0.wav     Directory containing members of 'class1'
  ├─── class1
  |    └─── instance4.wav
  |    └─── ...
  └─── class2.py              Directory containing members of 'class2'
       └─── instance20.wav
```

| Option   | Description | Default |
|----------|-------------|---------|
| `-lf`, `--label-file` | Указать целевой файл через запятую, содержащий метки для каждого файла *.wav*. Он должен содержать заголовок, а в первом столбце должно быть указано имя аудиофайла (с расширением!) | `None` |
| `-tc`, `--time-continuous` | Установить маркировку признаков в режиме непрерывного времени. Работает только в сочетании с `-t`, и указанный файл меток должен предоставлять метки для указанных прыжков во втором столбце. | `False` |
| `-el`, `--explicit-label` | Указать одну метку, которая будет явно использоваться для каждого входного файла. | `None` |
| `-nts`, `--no-timestamps` | Удалить метки времени с выхода. | Write timestamps in feature file. |
| `-nl`, `--no-labels` | Удалить метки из вывода. | Write labels in feature file. |

### Additional output
| Option   | Description | Default |
|----------|-------------|---------|
| `-so`, `--spectrogram-out` | Указать директорию где сохранять графики, используемых при извлечении, в формате `.png`. | `None` |
| `-wo`, `--wav-out` | Удобная функция для записи фрагментов аудиоданных, используемых при извлечении, в указанную папку. | `None` |

### Configuration and Help
| Option   | Description | Default |
|----------|-------------|---------|
| `-np`, `--number-of-processes` | Указать количество процессов, используемых для извлечения. По умолчанию количество доступных процессорных ядер | `None` |
| `-c`, `--config` | Путь к файлу конфигурации, используемому программой, можно указать здесь. Если файл еще не существует, он создается и заполняется стандартными настройками. | `deep.conf` |
| `--help` | Show help. | `None` |


### Extracting CNN-Descriptors from images

The tool also provides a commandline utility for extracting CNN descriptors from image data. It can be accessed through `deepspectrum image-features` with a reduced set of options. As with `deepspectrum features`, the first argument should be a folder containing the input image files (.png or .jpg). The available options are: `-o`, `-c`, `-np`, `-en`, `-fl`, `-bs`, `-lf`, `-el`,`-nl` and `--help`. These function the same as described above for `deepspectrum features`.
> Инструмент также предоставляет утилиту командной строки для извлечения дескрипторов CNN из данных изображения. Доступ к нему можно получить через `deepspectrum image-features` с ограниченным набором опций. Как и в случае с `deepspectrum features`, первым аргументом должен быть путь до директории, содержащей входные файлы изображений (`.png` или `.jpg`). Доступные параметры: `-o`, `-c`, `-np`, `-en`, `-fl`, `-bs`, `-lf`, `-el`, `-nl` и `--help`. Они функционируют так же, как описано выше для «функций deepspectrum».

[app]

# (str) Title of your application
title = X-chat-GPT

# (str) Package name
package.name = xchatgpt

# (str) Package domain (needed for android/ios packaging)
package.domain = com.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = venv,.git,.idea

# (list) List of exclusions using pattern matching
source.exclude_patterns =

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0,requests==2.31.0

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
# icon.filename = IMG_20250811_212447.jpg

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

# (list) List of service to declare
services =

#
# OSX Specific
#

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
presplash.color = #000000

# (list) Permissions
android.permissions = INTERNET

# (list) features (adds uses-feature -tags to manifest)
android.features =

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (str) Android asset directory. Default is the same as source.dir if not set
android.assets_dir = %(source.dir)s/assets

# (str) Android resource directory. Default is the same as source.dir if not set
android.res_dir =

# (list) Pattern to whitelist for the whole project
android.whitelist =

# (str) Path to a custom whitelist file
android.whitelist_src =

# (str) Path to a custom blacklist file
android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process.
android.add_jars =

# (list) List of Java files to add to the android project (can be java or aars)
# android.add_src = 

# (list) Android AAR archives to add
android.add_aars =

# (list) Gradle dependencies to add
android.gradle_dependencies =

# (list) Java classes to add as activities to the manifest.
android.add_activities =

# (str) python-for-android branch to use, defaults to master
# android.p4a_branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
ouya.category =

# (str) OUYA Console icon. It must be a 732x412 png image.
ouya.icon.filename =

# (str) OUYA Console banner. It must be a 1080x720 png image.
ouya.banner.filename =

# (str) Twitter integration
# twitter.consumer_key = YourConsumerKey
# twitter.consumer_secret = YourConsumerSecret

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios
# Alternative method to control code signing: specify your own codesign identity
# ios.codesign.identity = iPhone Developer

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = bins

#    -----------------------------------------------------------------------------#
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns. Instead of doing:
#
#    source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be written as:
#
#    [app:source.exclude_patterns]
#    license
#    data/audio/*.wav
#    data/images/original/*
#
#    -----------------------------------------------------------------------------#

# (list) Pattern to include in the zipfile
# [buildozer:zipinclude]
# patterns = .gitignore,LICENSE

# (list) Pattern to exclude from the zipfile
# [buildozer:zipexclude]
# patterns = .git,__pycache__

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.arch = armeabi-v7a

# (int) overrides automatic version detection (used in build number of apks)
# android.numeric_version = 1

# (str) The Android arch to build the srcaar for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.srcaar.arch = armeabi-v7a

# (str) The iOS arch to build for, choices: arm64, arm64e, i386, x86_64
# ios.arch = arm64

# (str) The iOS SDK version to use
# ios.sdk = 14.5

# (str) The first argument of ios-deploy. Default is the --justlaunch flag
# ios.deploy_args = --justlaunch

# (bool) Use --no counted flag for ios-deploy
# ios.deploy_no_counted = False

# (str) The Xcode project template to use
# ios.template = singleview

# (str) The Xcode project directory
# ios.project_dir = %(source.dir)s/ios

# (str) The Xcode project name
# ios.project_name = %(package.name)s

# (str) The Xcode scheme name
# ios.scheme_name = %(package.name)s

# (bool) Use bitcode when compiling
# ios.bitcode = True

# (bool) Use on-demand resources for ios
# ios.on_demand_resources = False

# (str) The path to the certificate for code signing
# ios.codesign.cert = ~/Library/MobileDevice/Certificates/*.p12

# (str) The password for the certificate
# ios.codesign.password =

# (str) The path to the provisioning profile
# ios.provisioning_profile = ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision

# (str) The team identifier
# ios.team_id =

# (str) The bundle identifier
# ios.bundle_id = %(package.domain)s.%(package.name)s

# (str) The application name
# ios.app_name = %(title)s

# (str) The version of the application
# ios.version = %(version)s

# (str) The build number
# ios.build_number = 1

# (str) The minimum iOS version supported
# ios.min_version = 11.0

# (str) The maximum iOS version supported
# ios.max_version =

# (str) The device family to target
# ios.device_family = iphone,ipad

# (bool) Enable auto-orientation
# ios.auto_orientation = True

# (bool) Enable status bar hidden
# ios.status_bar_hidden = False

# (str) The status bar style
# ios.status_bar_style = lightcontent

# (bool) Enable home indicator hidden (for iPhone X and later)
# ios.home_indicator_hidden = False

# (bool) Enable full screen
# ios.full_screen = False

# (bool) Enable UIFileSharingEnabled
# ios.file_sharing_enabled = False

# (bool) Enable UISupportsDocumentBrowser
# ios.document_browser_enabled = False

# (bool) Enable remote notifications
# ios.remote_notification = False

# (str) The path to the entitlements file
# ios.entitlements = %(source.dir)s/ios/Entitlements.plist

# (str) The path to the Info.plist file
# ios.info_plist = %(source.dir)s/ios/Info.plist

# (str) The path to the launch screen storyboard
# ios.launch_screen = %(source.dir)s/ios/LaunchScreen.storyboard

# (str) The path to the main storyboard
# ios.main_storyboard = %(source.dir)s/ios/Main.storyboard

# (str) The path to the asset catalog
# ios.asset_catalog = %(source.dir)s/ios/Assets.xcassets

# (str) The path to the iconset
# ios.iconset = %(source.dir)s/ios/AppIcon.appiconset

# (str) The path to the launch images
# ios.launch_images = %(source.dir)s/ios/LaunchImages.launchimage

# (str) The path to the xcconfig file
# ios.xcconfig = %(source.dir)s/ios/build.xcconfig

# (str) The path to the xcodebuild arguments file
# ios.xcodebuild_args = %(source.dir)s/ios/xcodebuild_args.txt

# (str) The path to the Podfile
# ios.podfile = %(source.dir)s/ios/Podfile

# (bool) Use CocoaPods
# ios.use_cocoapods = False

# (str) The path to the Carthage directory
# ios.carthage_dir = %(source.dir)s/ios/Carthage

# (bool) Use Carthage
# ios.use_carthage = False

# (str) The path to the Swift package manifest
# ios.swift_package_manifest = %(source.dir)s/ios/Package.swift

# (bool) Use Swift packages
# ios.use_swift_packages = False

# (str) The path to the WatchKit app
# ios.watchkit_app = %(source.dir)s/ios/WatchApp

# (str) The path to the WatchKit extension
# ios.watchkit_extension = %(source.dir)s/ios/WatchExtension

# (bool) Enable iMessage extension
# ios.imessage_extension = False

# (str) The path to the iMessage extension
# ios.imessage_extension_dir = %(source.dir)s/ios/MessageExtension

# (bool) Enable Siri extension
# ios.siri_extension = False

# (str) The path to the Siri extension
# ios.siri_extension_dir = %(source.dir)s/ios/SiriExtension

# (bool) Enable Today extension
# ios.today_extension = False

# (str) The path to the Today extension
# ios.today_extension_dir = %(source.dir)s/ios/TodayExtension

# (bool) Enable Notification Content extension
# ios.notification_content_extension = False

# (str) The path to the Notification Content extension
# ios.notification_content_extension_dir = %(source.dir)s/ios/NotificationContentExtension

# (bool) Enable Notification Service extension
# ios.notification_service_extension = False

# (str) The path to the Notification Service extension
# ios.notification_service_extension_dir = %(source.dir)s/ios/NotificationServiceExtension

# (bool) Enable Share extension
# ios.share_extension = False

# (str) The path to the Share extension
# ios.share_extension_dir = %(source.dir)s/ios/ShareExtension

# (bool) Enable Action extension
# ios.action_extension = False

# (str) The path to the Action extension
# ios.action_extension_dir = %(source.dir)s/ios/ActionExtension

# (bool) Enable Photo Editing extension
# ios.photo_editing_extension = False

# (str) The path to the Photo Editing extension
# ios.photo_editing_extension_dir = %(source.dir)s/ios/PhotoEditingExtension

# (bool) Enable File Provider extension
# ios.file_provider_extension = False

# (str) The path to the File Provider extension
# ios.file_provider_extension_dir = %(source.dir)s/ios/FileProviderExtension

# (bool) Enable Network Extension
# ios.network_extension = False

# (str) The path to the Network Extension
# ios.network_extension_dir = %(source.dir)s/ios/NetworkExtension

# (bool) Enable Intents extension
# ios.intents_extension = False

# (str) The path to the Intents extension
# ios.intents_extension_dir = %(source.dir)s/ios/IntentsExtension

# (bool) Enable Intents UI extension
# ios.intents_ui_extension = False

# (str) The path to the Intents UI extension
# ios.intents_ui_extension_dir = %(source.dir)s/ios/IntentsUIExtension

# (bool) Enable CallKit
# ios.callkit = False

# (bool) Enable ARKit
# ios.arkit = False

# (bool) Enable CoreML
# ios.coreml = False

# (bool) Enable HealthKit
# ios.healthkit = False

# (bool) Enable HomeKit
# ios.homekit = False

# (bool) Enable MapKit
# ios.mapkit = False

# (bool) Enable Metal
# ios.metal = False

# (bool) Enable MLKit
# ios.mlkit = False

# (bool) Enable RealityKit
# ios.realitykit = False

# (bool) Enable SceneKit
# ios.scenekit = False

# (bool) Enable SpriteKit
# ios.spritekit = False

# (bool) Enable StoreKit
# ios.storekit = False

# (bool) Enable Vision
# ios.vision = False

# (bool) Enable WatchConnectivity
# ios.watchconnectivity = False

# (bool) Enable WidgetKit
# ios.widgetkit = False

# (bool) Enable CoreMotion
# ios.coremotion = False

# (bool) Enable CoreLocation
# ios.corelocation = False

# (bool) Enable CoreBluetooth
# ios.corebluetooth = False

# (bool) Enable CoreNFC
# ios.corenfc = False

# (bool) Enable CoreMedia
# ios.coremedia = False

# (bool) Enable AVFoundation
# ios.avfoundation = False

# (bool) Enable AVKit
# ios.avkit = False

# (bool) Enable WebKit
# ios.webkit = False

# (bool) Enable JavaScriptCore
# ios.javascriptcore = False

# (bool) Enable FileProvider
# ios.fileprovider = False

# (bool) Enable UserNotifications
# ios.usernotifications = False

# (bool) Enable PushKit
# ios.pushkit = False

# (bool) Enable BackgroundTasks
# ios.backgroundtasks = False

# (bool) Enable BackgroundFetch
# ios.backgroundfetch = False

# (bool) Enable RemoteViews
# ios.remoteviews = False

# (bool) Enable QuickLook
# ios.quicklook = False

# (bool) Enable PDFKit
# ios.pdfkit = False

# (bool) Enable MessageUI
# ios.messageui = False

# (bool) Enable ContactsUI
# ios.contactsui = False

# (bool) Enable EventKitUI
# ios.eventkitui = False

# (bool) Enable HealthUI
# ios.healthui = False

# (bool) Enable HomeUI
# ios.homeui = False

# (bool) Enable MapUI
# ios.mapui = False

# (bool) Enable PassKitUI
# ios.passkitui = False

# (bool) Enable PhotosUI
# ios.photosui = False

# (bool) Enable ReplayKitUI
# ios.replaykitui = False

# (bool) Enable SpeechUI
# ios.speechui = False

# (bool) Enable StoreKitUI
# ios.storekitui = False

# (bool) Enable TVUIKit
# ios.tvuikit = False

# (bool) Enable UIKit
# ios.uikit = True

# (bool) Enable WatchKit
# ios.watchkit = False

# (bool) Enable VisionKit
# ios.visionkit = False

# (bool) Enable XCTest
# ios.xctest = False

# (bool) Enable os_log
# ios.os_log = False

# (bool) Enable libc++
# ios.libcxx = True

# (bool) Enable libz
# ios.libz = True

# (bool) Enable libsqlite3
# ios.libsqlite3 = True

# (bool) Enable libcrypto
# ios.libcrypto = False

# (bool) Enable libssl
# ios.libssl = False

# (bool) Enable libffi
# ios.libffi = True

# (bool) Enable libpng
# ios.libpng = True

# (bool) Enable libjpeg
# ios.libjpeg = True

# (bool) Enable libtiff
# ios.libtiff = False

# (bool) Enable libwebp
# ios.libwebp = False

# (bool) Enable liblzma
# ios.liblzma = False

# (bool) Enable libxml2
# ios.libxml2 = True

# (bool) Enable libxslt
# ios.libxslt = False

# (bool) Enable libcurl
# ios.libcurl = True

# (bool) Enable libiconv
# ios.libiconv = True

# (bool) Enable libintl
# ios.libintl = False

# (bool) Enable libffi
# ios.libffi = True

# (bool) Enable libusb
# ios.libusb = False

# (bool) Enable libudev
# ios.libudev = False

# (bool) Enable libpulse
# ios.libpulse = False

# (bool) Enable libasound
# ios.libasound = False

# (bool) Enable libao
# ios.libao = False

# (bool) Enable libsdl2
# ios.libsdl2 = False

# (bool) Enable libsdl2_image
# ios.libsdl2_image = False

# (bool) Enable libsdl2_mixer
# ios.libsdl2_mixer = False

# (bool) Enable libsdl2_ttf
# ios.libsdl2_ttf = False

# (bool) Enable libsdl2_net
# ios.libsdl2_net = False

# (bool) Enable libgstreamer
# ios.libgstreamer = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopenal
# ios.libopenal = False

# (bool) Enable libvorbis
# ios.libvorbis = False

# (bool) Enable libogg
# ios.libogg = False

# (bool) Enable libtheora
# ios.libtheora = False

# (bool) Enable libvpx
# ios.libvpx = False

# (bool) Enable libx264
# ios.libx264 = False

# (bool) Enable libxvid
# ios.libxvid = False

# (bool) Enable libfaac
# ios.libfaac = False

# (bool) Enable libmp3lame
# ios.libmp3lame = False

# (bool) Enable libopus
# ios.libopus = False

# (bool) Enable libspeex
# ios.libspeex = False

# (bool) Enable libflac
# ios.libflac = False

# (bool) Enable libwavpack
# ios.libwavpack = False

# (bool) Enable libmodplug
# ios.libmodplug = False

# (bool) Enable libass
# ios.libass = False

# (bool) Enable libbluray
# ios.libbluray = False

# (bool) Enable libdvdnav
# ios.libdvdnav = False

# (bool) Enable libdvdread
# ios.libdvdread = False

# (bool) Enable libmad
# ios.libmad = False

# (bool) Enable libmpeg2
# ios.libmpeg2 = False

# (bool) Enable libmpeg3
# ios.libmpeg3 = False

# (bool) Enable libmpg123
# ios.libmpg123 = False

# (bool) Enable libvorbisidec
# ios.libvorbisidec = False

# (bool) Enable liba52
# ios.liba52 = False

# (bool) Enable libdc1394
# ios.libdc1394 = False

# (bool) Enable libraw1394
# ios.libraw1394 = False

# (bool) Enable libavc1394
# ios.libavc1394 = False

# (bool) Enable libiec61883
# ios.libiec61883 = False

# (bool) Enable lib火线
# ios.libfirewire = False

# (bool) Enable libcanberra
# ios.libcanberra = False

# (bool) Enable libespeak
# ios.libespeak = False

# (bool) Enable libflite
# ios.libflite = False

# (bool) Enable libttspico
# ios.libttspico = False

# (bool) Enable libfreetype
# ios.libfreetype = True

# (bool) Enable libharfbuzz
# ios.libharfbuzz = False

# (bool) Enable libgraphite2
# ios.libgraphite2 = False

# (bool) Enable libicu
# ios.libicu = False

# (bool) Enable libboost
# ios.libboost = False

# (bool) Enable libeigen
# ios.libeigen = False

# (bool) Enable libgmp
# ios.libgmp = False

# (bool) Enable libmpfr
# ios.libmpfr = False

# (bool) Enable libmpc
# ios.libmpc = False

# (bool) Enable libsodium
# ios.libsodium = False

# (bool) Enable libzmq
# ios.libzmq = False

# (bool) Enable libprotobuf
# ios.libprotobuf = False

# (bool) Enable libprotoc
# ios.libprotoc = False

# (bool) Enable libgrpc
# ios.libgrpc = False

# (bool) Enable libjsoncpp
# ios.libjsoncpp = False

# (bool) Enable libyajl
# ios.libtajl = False

# (bool) Enable libxmlsec1
# ios.libxmlsec1 = False

# (bool) Enable libxslt
# ios.libxslt = False

# (bool) Enable libyaml
# ios.libyaml = False

# (bool) Enable libzip
# ios.libzip = False

# (bool) Enable libzstd
# ios.libzstd = False

# (bool) Enable liblz4
# ios.liblz4 = False

# (bool) Enable libsnappy
# ios.libsnappy = False

# (bool) Enable liblzo2
# ios.liblzo2 = False

# (bool) Enable libbz2
# ios.libbz2 = True

# (bool) Enable libsqlite3
# ios.libsqlite3 = True

# (bool) Enable libmysqlclient
# ios.libmysqlclient = False

# (bool) Enable libpq
# ios.libpq = False

# (bool) Enable libiodbc
# ios.libiodbc = False

# (bool) Enable libsqliteodbc
# ios.libsqliteodbc = False

# (bool) Enable libmariadbclient
# ios.libmariadbclient = False

# (bool) Enable libmongoc
# ios.libmongoc = False

# (bool) Enable libbson
# ios.libbson = False

# (bool) Enable libredis
# ios.libredis = False

# (bool) Enable libmemcached
# ios.libmemcached = False

# (bool) Enable liblmdb
# ios.liblmdb = False

# (bool) Enable libleveldb
# ios.libleveldb = False

# (bool) Enable librocksdb
# ios.librocksdb = False

# (bool) Enable libcassandra
# ios.libcassandra = False

# (bool) Enable liborientdb
# ios.liborientdb = False

# (bool) Enable libneo4j-client
# ios.libneo4j_client = False

# (bool) Enable libdrizzle
# ios.libdrizzle = False

# (bool) Enable libfirebird
# ios.libfirebird = False

# (bool) Enable libfreetds
# ios.libfreetds = False

# (bool) Enable libmaxminddb
# ios.libmaxminddb = False

# (bool) Enable libpqxx
# ios.libpqxx = False

# (bool) Enable libsqlite3pp
# ios.libsqlite3pp = False

# (bool) Enable libsqlcipher
# ios.libsqlcipher = False

# (bool) Enable libtbb
# ios.libtbb = False

# (bool) Enable libopenmp
# ios.libopenmp = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenblas
# ios.libopenblas = False

# (bool) Enable liblapack
# ios.liblapack = False

# (bool) Enable libblas
# ios.libblas = False

# (bool) Enable libarpack
# ios.libarpack = False

# (bool) Enable libsuperlu
# ios.libsuperlu = False

# (bool) Enable libumfpack
# ios.libumfpack = False

# (bool) Enable libcholmod
# ios.libcholmod = False

# (bool) Enable libcxsparse
# ios.libcxsparse = False

# (bool) Enable libccolamd
# ios.libccolamd = False

# (bool) Enable libcamd
# ios.libcamd = False

# (bool) Enable libcolamd
# ios.libcolamd = False

# (bool) Enable libamd
# ios.libamd = False

# (bool) Enable libsuitesparseconfig
# ios.libsuitesparseconfig = False

# (bool) Enable libmetis
# ios.libmetis = False

# (bool) Enable libptscotch
# ios.libptscotch = False

# (bool) Enable libscotch
# ios.libscotch = False

# (bool) Enable libhypre
# ios.libhypre = False

# (bool) Enable libpetsc
# ios.libpetsc = False

# (bool) Enable libslepc
# ios.libslepc = False

# (bool) Enable libtrilinos
# ios.libtrilinos = False

# (bool) Enable libdealii
# ios.libdealii = False

# (bool) Enable libdolfin
# ios.libdolfin = False

# (bool) Enable libfenics
# ios.libfenics = False

# (bool) Enable libfreefem++
# ios.libfreefem++ = False

# (bool) Enable libgmsh
# ios.libgmsh = False

# (bool) Enable liboce
# ios.liboce = False

# (bool) Enable libopencascade
# ios.libopencascade = False

# (bool) Enable libparaview
# ios.libparaview = False

# (bool) Enable libvtk
# ios.libvtk = False

# (bool) Enable libitk
# ios.libitk = False

# (bool) Enable libmitk
# ios.libmitk = False

# (bool) Enable libinsightseg
# ios.libinsightseg = False

# (bool) Enable libgdcm
# ios.libgdcm = False

# (bool) Enable libdcmtk
# ios.libdcmtk = False

# (bool) Enable libopenslide
# ios.libopenslide = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

#
# Android specific section
#

[android]
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
olive, purple, silver, teal.
presplash.color = #6a0080

# (list) Permissions
android.permissions = INTERNET

# (list) features (adds uses-feature -tags to manifest)
android.features =

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 31

# (str) Android NDK version to use
android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support,
it should usually match android.minapi.
android.ndk_api = 21

# (str) Android asset directory. Default is the same as source.dir if not set
android.assets_dir = %(source.dir)s/assets

# (str) Android resource directory. Default is the same as source.dir if not set
android.res_dir =

# (list) Pattern to whitelist for the whole project
android.whitelist =

# (str) Path to a custom whitelist file
android.whitelist_src =

# (str) Path to a custom blacklist file
android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
their classes. Don't add jars that you do not need, since extra jars can slow
down the build process.
android.add_jars =

# (list) List of Java files to add to the android project (can be java or aars)
android.add_src =

# (list) Android AAR archives to add
android.add_aars =

# (list) Gradle dependencies to add
android.gradle_dependencies =

# (list) Java classes to add as activities to the manifest.
android.add_activities =

# (str) python-for-android branch to use, defaults to master
# android.p4a_branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
ouya.category =

# (str) OUYA Console icon. It must be a 732x412 png image.
ouya.icon.filename =

# (str) OUYA Console banner. It must be a 1080x720 png image.
ouya.banner.filename =

# (str) Twitter integration
# twitter.consumer_key = YourConsumerKey
# twitter.consumer_secret = YourConsumerSecret

#
# iOS specific section
#

[ios]
# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios
# Alternative method to control code signing: specify your own codesign identity
# ios.codesign.identity = iPhone Developer

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: buildozer ios list_identities
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = %(ios.codesign.debug)s

# (str) The iOS SDK version to use
# ios.sdk = 14.5

# (str) The first argument of ios-deploy. Default is the --justlaunch flag
# ios.deploy_args = --justlaunch

# (bool) Use --no counted flag for ios-deploy
# ios.deploy_no_counted = False

# (str) The Xcode project template to use
# ios.template = singleview

# (str) The Xcode project directory
# ios.project_dir = %(source.dir)s/ios

# (str) The Xcode project name
# ios.project_name = %(package.name)s

# (str) The Xcode scheme name
# ios.scheme_name = %(package.name)s

# (bool) Use bitcode when compiling
# ios.bitcode = True

# (bool) Use on-demand resources for ios
# ios.on_demand_resources = False

# (str) The path to the certificate for code signing
# ios.codesign.cert = ~/Library/MobileDevice/Certificates/*.p12

# (str) The password for the certificate
# ios.codesign.password =

# (str) The path to the provisioning profile
# ios.provisioning_profile = ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision

# (str) The team identifier
# ios.team_id =

# (str) The bundle identifier
# ios.bundle_id = %(package.domain)s.%(package.name)s

# (str) The application name
# ios.app_name = %(title)s

# (str) The version of the application
# ios.version = %(version)s

# (str) The build number
# ios.build_number = 1

# (str) The minimum iOS version supported
# ios.min_version = 11.0

# (str) The maximum iOS version supported
# ios.max_version =

# (str) The device family to target
# ios.device_family = iphone,ipad

# (bool) Enable auto-orientation
# ios.auto_orientation = True

# (bool) Enable status bar hidden
# ios.status_bar_hidden = False

# (str) The status bar style
# ios.status_bar_style = lightcontent

# (bool) Enable home indicator hidden (for iPhone X and later)
# ios.home_indicator_hidden = False

# (bool) Enable full screen
# ios.full_screen = False

# (bool) Enable UIFileSharingEnabled
# ios.file_sharing_enabled = False

# (bool) Enable UISupportsDocumentBrowser
# ios.document_browser_enabled = False

# (bool) Enable remote notifications
# ios.remote_notification = False

# (str) The path to the entitlements file
# ios.entitlements = %(source.dir)s/ios/Entitlements.plist

# (str) The path to the Info.plist file
# ios.info_plist = %(source.dir)s/ios/Info.plist

# (str) The path to the launch screen storyboard
# ios.launch_screen = %(source.dir)s/ios/LaunchScreen.storyboard

# (str) The path to the main storyboard
# ios.main_storyboard = %(source.dir)s/ios/Main.storyboard

# (str) The path to the asset catalog
# ios.asset_catalog = %(source.dir)s/ios/Assets.xcassets

# (str) The path to the iconset
# ios.iconset = %(source.dir)s/ios/AppIcon.appiconset

# (str) The path to the launch images
# ios.launch_images = %(source.dir)s/ios/LaunchImages.launchimage

# (str) The path to the xcconfig file
# ios.xcconfig = %(source.dir)s/ios/build.xcconfig

# (str) The path to the xcodebuild arguments file
# ios.xcodebuild_args = %(source.dir)s/ios/xcodebuild_args.txt

# (str) The path to the Podfile
# ios.podfile = %(source.dir)s/ios/Podfile

# (bool) Use CocoaPods
# ios.use_cocoapods = False

# (str) The path to the Carthage directory
# ios.carthage_dir = %(source.dir)s/ios/Carthage

# (bool) Use Carthage
# ios.use_carthage = False

# (str) The path to the Swift package manifest
# ios.swift_package_manifest = %(source.dir)s/ios/Package.swift

# (bool) Use Swift packages
# ios.use_swift_packages = False

# (str) The path to the WatchKit app
# ios.watchkit_app = %(source.dir)s/ios/WatchApp

# (str) The path to the WatchKit extension
# ios.watchkit_extension = %(source.dir)s/ios/WatchExtension

# (bool) Enable iMessage extension
# ios.imessage_extension = False

# (str) The path to the iMessage extension
# ios.imessage_extension_dir = %(source.dir)s/ios/MessageExtension

# (bool) Enable Siri extension
# ios.siri_extension = False

# (str) The path to the Siri extension
# ios.siri_extension_dir = %(source.dir)s/ios/SiriExtension

# (bool) Enable Today extension
# ios.today_extension = False

# (str) The path to the Today extension
# ios.today_extension_dir = %(source.dir)s/ios/TodayExtension

# (bool) Enable Notification Content extension
# ios.notification_content_extension = False

# (str) The path to the Notification Content extension
# ios.notification_content_extension_dir = %(source.dir)s/ios/NotificationContentExtension

# (bool) Enable Notification Service extension
# ios.notification_service_extension = False

# (str) The path to the Notification Service extension
# ios.notification_service_extension_dir = %(source.dir)s/ios/NotificationServiceExtension

# (bool) Enable Share extension
# ios.share_extension = False

# (str) The path to the Share extension
# ios.share_extension_dir = %(source.dir)s/ios/ShareExtension

# (bool) Enable Action extension
# ios.action_extension = False

# (str) The path to the Action extension
# ios.action_extension_dir = %(source.dir)s/ios/ActionExtension

# (bool) Enable Photo Editing extension
# ios.photo_editing_extension = False

# (str) The path to the Photo Editing extension
# ios.photo_editing_extension_dir = %(source.dir)s/ios/PhotoEditingExtension

# (bool) Enable File Provider extension
# ios.file_provider_extension = False

# (str) The path to the File Provider extension
# ios.file_provider_extension_dir = %(source.dir)s/ios/FileProviderExtension

# (bool) Enable Network Extension
# ios.network_extension = False

# (str) The path to the Network Extension
# ios.network_extension_dir = %(source.dir)s/ios/NetworkExtension

# (bool) Enable Intents extension
# ios.intents_extension = False

# (str) The path to the Intents extension
# ios.intents_extension_dir = %(source.dir)s/ios/IntentsExtension

# (bool) Enable Intents UI extension
# ios.intents_ui_extension = False

# (str) The path to the Intents UI extension
# ios.intents_ui_extension_dir = %(source.dir)s/ios/IntentsUIExtension

# (bool) Enable CallKit
# ios.callkit = False

# (bool) Enable ARKit
# ios.arkit = False

# (bool) Enable CoreML
# ios.coreml = False

# (bool) Enable HealthKit
# ios.healthkit = False

# (bool) Enable HomeKit
# ios.homekit = False

# (bool) Enable MapKit
# ios.mapkit = False

# (bool) Enable Metal
# ios.metal = False

# (bool) Enable MLKit
# ios.mlkit = False

# (bool) Enable RealityKit
# ios.realitykit = False

# (bool) Enable SceneKit
# ios.scenekit = False

# (bool) Enable SpriteKit
# ios.spritekit = False

# (bool) Enable StoreKit
# ios.storekit = False

# (bool) Enable Vision
# ios.vision = False

# (bool) Enable WatchConnectivity
# ios.watchconnectivity = False

# (bool) Enable WidgetKit
# ios.widgetkit = False

# (bool) Enable CoreMotion
# ios.coremotion = False

# (bool) Enable CoreLocation
# ios.corelocation = False

# (bool) Enable CoreBluetooth
# ios.corebluetooth = False

# (bool) Enable CoreNFC
# ios.corenfc = False

# (bool) Enable CoreMedia
# ios.coremedia = False

# (bool) Enable AVFoundation
# ios.avfoundation = False

# (bool) Enable AVKit
# ios.avkit = False

# (bool) Enable WebKit
# ios.webkit = False

# (bool) Enable JavaScriptCore
# ios.javascriptcore = False

# (bool) Enable FileProvider
# ios.fileprovider = False

# (bool) Enable UserNotifications
# ios.usernotifications = False

# (bool) Enable PushKit
# ios.pushkit = False

# (bool) Enable BackgroundTasks
# ios.backgroundtasks = False

# (bool) Enable BackgroundFetch
# ios.backgroundfetch = False

# (bool) Enable RemoteViews
# ios.remoteviews = False

# (bool) Enable QuickLook
# ios.quicklook = False

# (bool) Enable PDFKit
# ios.pdfkit = False

# (bool) Enable MessageUI
# ios.messageui = False

# (bool) Enable ContactsUI
# ios.contactsui = False

# (bool) Enable EventKitUI
# ios.eventkitui = False

# (bool) Enable HealthUI
# ios.healthui = False

# (bool) Enable HomeUI
# ios.homeui = False

# (bool) Enable MapUI
# ios.mapui = False

# (bool) Enable PassKitUI
# ios.passkitui = False

# (bool) Enable PhotosUI
# ios.photosui = False

# (bool) Enable ReplayKitUI
# ios.replaykitui = False

# (bool) Enable SpeechUI
# ios.speechui = False

# (bool) Enable StoreKitUI
# ios.storekitui = False

# (bool) Enable TVUIKit
# ios.tvuikit = False

# (bool) Enable UIKit
# ios.uikit = True

# (bool) Enable WatchKit
# ios.watchkit = False

# (bool) Enable VisionKit
# ios.visionkit = False

# (bool) Enable XCTest
# ios.xctest = False

# (bool) Enable os_log
# ios.os_log = False

# (bool) Enable libc++
# ios.libcxx = True

# (bool) Enable libz
# ios.libz = True

# (bool) Enable libsqlite3
# ios.libsqlite3 = True

# (bool) Enable libcrypto
# ios.libcrypto = False

# (bool) Enable libssl
# ios.libssl = False

# (bool) Enable libffi
# ios.libffi = True

# (bool) Enable libpng
# ios.libpng = True

# (bool) Enable libjpeg
# ios.libjpeg = True

# (bool) Enable libtiff
# ios.libtiff = False

# (bool) Enable libwebp
# ios.libwebp = False

# (bool) Enable liblzma
# ios.liblzma = False

# (bool) Enable libxml2
# ios.libxml2 = True

# (bool) Enable libxslt
# ios.libxslt = False

# (bool) Enable libcurl
# ios.libcurl = True

# (bool) Enable libiconv
# ios.libiconv = True

# (bool) Enable libintl
# ios.libintl = False

# (bool) Enable libffi
# ios.libffi = True

# (bool) Enable libusb
# ios.libusb = False

# (bool) Enable libudev
# ios.libudev = False

# (bool) Enable libpulse
# ios.libpulse = False

# (bool) Enable libasound
# ios.libasound = False

# (bool) Enable libao
# ios.libao = False

# (bool) Enable libsdl2
# ios.libsdl2 = False

# (bool) Enable libsdl2_image
# ios.libsdl2_image = False

# (bool) Enable libsdl2_mixer
# ios.libsdl2_mixer = False

# (bool) Enable libsdl2_ttf
# ios.libsdl2_ttf = False

# (bool) Enable libsdl2_net
# ios.libsdl2_net = False

# (bool) Enable libgstreamer
# ios.libgstreamer = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopenal
# ios.libopenal = False

# (bool) Enable libvorbis
# ios.libvorbis = False

# (bool) Enable libogg
# ios.libogg = False

# (bool) Enable libtheora
# ios.libtheora = False

# (bool) Enable libvpx
# ios.libvpx = False

# (bool) Enable libx264
# ios.libx264 = False

# (bool) Enable libxvid
# ios.libxvid = False

# (bool) Enable libfaac
# ios.libfaac = False

# (bool) Enable libmp3lame
# ios.libmp3lame = False

# (bool) Enable libopus
# ios.libopus = False

# (bool) Enable libspeex
# ios.libspeex = False

# (bool) Enable libflac
# ios.libflac = False

# (bool) Enable libwavpack
# ios.libwavpack = False

# (bool) Enable libmodplug
# ios.libmodplug = False

# (bool) Enable libass
# ios.libass = False

# (bool) Enable libbluray
# ios.libbluray = False

# (bool) Enable libdvdnav
# ios.libdvdnav = False

# (bool) Enable libdvdread
# ios.libdvdread = False

# (bool) Enable libmad
# ios.libmad = False

# (bool) Enable libmpeg2
# ios.libmpeg2 = False

# (bool) Enable libmpeg3
# ios.libmpeg3 = False

# (bool) Enable libmpg123
# ios.libmpg123 = False

# (bool) Enable libvorbisidec
# ios.libvorbisidec = False

# (bool) Enable liba52
# ios.liba52 = False

# (bool) Enable libdc1394
# ios.libdc1394 = False

# (bool) Enable libraw1394
# ios.libraw1394 = False

# (bool) Enable libavc1394
# ios.libavc1394 = False

# (bool) Enable libiec61883
# ios.libiec61883 = False

# (bool) Enable lib火线
# ios.libfirewire = False

# (bool) Enable libcanberra
# ios.libcanberra = False

# (bool) Enable libespeak
# ios.libespeak = False

# (bool) Enable libflite
# ios.libflite = False

# (bool) Enable libttspico
# ios.libttspico = False

# (bool) Enable libfreetype
# ios.libfreetype = True

# (bool) Enable libharfbuzz
# ios.libharfbuzz = False

# (bool) Enable libgraphite2
# ios.libgraphite2 = False

# (bool) Enable libicu
# ios.libicu = False

# (bool) Enable libboost
# ios.libboost = False

# (bool) Enable libeigen
# ios.libeigen = False

# (bool) Enable libgmp
# ios.libgmp = False

# (bool) Enable libmpfr
# ios.libmpfr = False

# (bool) Enable libmpc
# ios.libmpc = False

# (bool) Enable libsodium
# ios.libsodium = False

# (bool) Enable libzmq
# ios.libzmq = False

# (bool) Enable libprotobuf
# ios.libprotobuf = False

# (bool) Enable libprotoc
# ios.libprotoc = False

# (bool) Enable libgrpc
# ios.libgrpc = False

# (bool) Enable libjsoncpp
# ios.libjsoncpp = False

# (bool) Enable libyajl
# ios.libtajl = False

# (bool) Enable libxmlsec1
# ios.libxmlsec1 = False

# (bool) Enable libxslt
# ios.libxslt = False

# (bool) Enable libyaml
# ios.libyaml = False

# (bool) Enable libzip
# ios.libzip = False

# (bool) Enable libzstd
# ios.libzstd = False

# (bool) Enable liblz4
# ios.liblz4 = False

# (bool) Enable libsnappy
# ios.libsnappy = False

# (bool) Enable liblzo2
# ios.liblzo2 = False

# (bool) Enable libbz2
# ios.libbz2 = True

# (bool) Enable libsqlite3
# ios.libsqlite3 = True

# (bool) Enable libmysqlclient
# ios.libmysqlclient = False

# (bool) Enable libpq
# ios.libpq = False

# (bool) Enable libiodbc
# ios.libiodbc = False

# (bool) Enable libsqliteodbc
# ios.libsqliteodbc = False

# (bool) Enable libmariadbclient
# ios.libmariadbclient = False

# (bool) Enable libmongoc
# ios.libmongoc = False

# (bool) Enable libbson
# ios.libbson = False

# (bool) Enable libredis
# ios.libredis = False

# (bool) Enable libmemcached
# ios.libmemcached = False

# (bool) Enable liblmdb
# ios.liblmdb = False

# (bool) Enable libleveldb
# ios.libleveldb = False

# (bool) Enable librocksdb
# ios.librocksdb = False

# (bool) Enable libcassandra
# ios.libcassandra = False

# (bool) Enable liborientdb
# ios.liborientdb = False

# (bool) Enable libneo4j-client
# ios.libneo4j_client = False

# (bool) Enable libdrizzle
# ios.libdrizzle = False

# (bool) Enable libfirebird
# ios.libfirebird = False

# (bool) Enable libfreetds
# ios.libfreetds = False

# (bool) Enable libmaxminddb
# ios.libmaxminddb = False

# (bool) Enable libpqxx
# ios.libpqxx = False

# (bool) Enable libsqlite3pp
# ios.libsqlite3pp = False

# (bool) Enable libsqlcipher
# ios.libsqlcipher = False

# (bool) Enable libtbb
# ios.libtbb = False

# (bool) Enable libopenmp
# ios.libopenmp = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenblas
# ios.libopenblas = False

# (bool) Enable liblapack
# ios.liblapack = False

# (bool) Enable libblas
# ios.libblas = False

# (bool) Enable libarpack
# ios.libarpack = False

# (bool) Enable libsuperlu
# ios.libsuperlu = False

# (bool) Enable libumfpack
# ios.libumfpack = False

# (bool) Enable libcholmod
# ios.libcholmod = False

# (bool) Enable libcxsparse
# ios.libcxsparse = False

# (bool) Enable libccolamd
# ios.libccolamd = False

# (bool) Enable libcamd
# ios.libcamd = False

# (bool) Enable libcolamd
# ios.libcolamd = False

# (bool) Enable libamd
# ios.libamd = False

# (bool) Enable libsuitesparseconfig
# ios.libsuitesparseconfig = False

# (bool) Enable libmetis
# ios.libmetis = False

# (bool) Enable libptscotch
# ios.libptscotch = False

# (bool) Enable libscotch
# ios.libscotch = False

# (bool) Enable libhypre
# ios.libhypre = False

# (bool) Enable libpetsc
# ios.libpetsc = False

# (bool) Enable libslepc
# ios.libslepc = False

# (bool) Enable libtrilinos
# ios.libtrilinos = False

# (bool) Enable libdealii
# ios.libdealii = False

# (bool) Enable libdolfin
# ios.libdolfin = False

# (bool) Enable libfenics
# ios.libfenics = False

# (bool) Enable libfreefem++
# ios.libfreefem++ = False

# (bool) Enable libgmsh
# ios.libgmsh = False

# (bool) Enable liboce
# ios.liboce = False

# (bool) Enable libopencascade
# ios.libopencascade = False

# (bool) Enable libparaview
# ios.libparaview = False

# (bool) Enable libvtk
# ios.libvtk = False

# (bool) Enable libitk
# ios.libitk = False

# (bool) Enable libmitk
# ios.libmitk = False

# (bool) Enable libinsightseg
# ios.libinsightseg = False

# (bool) Enable libgdcm
# ios.libgdcm = False

# (bool) Enable libdcmtk
# ios.libdcmtk = False

# (bool) Enable libopenslide
# ios.libopenslide = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False


# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
# ios.libmoveit = False

# (bool) Enable librviz
# ios.librviz = False

# (bool) Enable libopencv
# ios.libopencv = False

# (bool) Enable libopencv_contrib
# ios.libopencv_contrib = False

# (bool) Enable libopenni
# ios.libopenni = False

# (bool) Enable libopenni2
# ios.libopenni2 = False

# (bool) Enable libfreenect
# ios.libfreenect = False

# (bool) Enable librealsense
# ios.librealsense = False

# (bool) Enable libzed
# ios.libzed = False

# (bool) Enable libpcl
# ios.libpcl = False

# (bool) Enable libfcl
# ios.libfcl = False

# (bool) Enable libassimp
# ios.libassimp = False

# (bool) Enable libbullet
# ios.libbullet = False

# (bool) Enable libode
# ios.libode = False

# (bool) Enable libphysx
# ios.libphysx = False

# (bool) Enable libhavok
# ios.libhavok = False

# (bool) Enable libbox2d
# ios.libbox2d = False

# (bool) Enable libchipmunk
# ios.libchipmunk = False

# (bool) Enable libelastic
# ios.libelastic = False

# (bool) Enable libfluid
# ios.libfluid = False

# (bool) Enable libmujoco
# ios.libmujoco = False

# (bool) Enable libdart
# ios.libdart = False

# (bool) Enable libopensim
# ios.libopensim = False

# (bool) Enable libsimbody
# ios.libsimbody = False

# (bool) Enable libgazebo
# ios.libgazebo = False

# (bool) Enable libros
# ios.libros = False

# (bool) Enable libros_comm
# ios.libros_comm = False

# (bool) Enable libroscpp
# ios.libroscpp = False

# (bool) Enable librospy
# ios.librospy = False

# (bool) Enable libtf
# ios.libtf = False

# (bool) Enable libtf2
# ios.libtf2 = False

# (bool) Enable liburdf
# ios.liburdf = False

# (bool) Enable libmoveit
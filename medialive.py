from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
import re
import boto3
import time
def geturl(channel_id):
    client = boto3.client('medialive',region_name='ap-south-1')
    status = client.describe_channel(
        ChannelId=channel_id
    )
    for var in status['Destinations'][1]["Settings"]:
        url = (var['Url'])
    return url
def stopedstatus(channel_id):
    client = boto3.client('medialive',region_name='ap-south-1')
    for i in range(1, 1000):
        sta = client.describe_channel(
            ChannelId=channel_id
        )
        val = sta['State']
        if sta['State'] == 'IDLE' or sta['State'] == 'RUNNING':
            val = sta['State']
            return val
            break
    return val
def getstatus(val,channelid):
    client = boto3.client('medialive',region_name='ap-south-1')
    status = client.describe_channel(
        ChannelId=channelid
    )
    for key, value in status.items():
        if val == key:

            return value
def emergency_stop(ID):
    client = boto3.client('medialive', region_name='ap-south-1')
    ID = ID
    response = client.list_channels(
        MaxResults=123,

    )
    for i in response['Channels']:
        if i['Name'] == ID:
            id = i['Id']
            return id
    return 0
def inputId(merchant_id, live_name, live_id):
    client = boto3.client('medialive',region_name='ap-south-1')
    response = client.list_inputs(
        MaxResults=123,

    )
    size = len(response['Inputs'])
    Input = {
        "ID": merchant_id,
        "input_type": "RTMP_PUSH",
        "bitrate": "MAX_10_MBPS",
        "resolution": "SD"
    }
    id = Input['ID']

    def rtmp_push(client, Id, sg):
        response = client.create_input(
            Type="RTMP_PUSH",
            InputSecurityGroups=[sg],
            Destinations=[
                {'StreamName': "{}/{}".format(live_name, live_id)}],
            Name=live_name)
        return response

    #
    def input_sg(client):
        try:
            response = client.list_input_security_groups()['InputSecurityGroups']
            return response[0]['Id']
        except IndexError:
            response = client.create_input_security_group(
                WhitelistRules=[
                    {"Cidr": "0.0.0.0/0"}
                ])

            return response['SecurityGroup']['Id']

    if Input['input_type'] == 'RTMP_PUSH':
        if size < 5:
            input = rtmp_push(client, id, input_sg(client))
            input_id = input['Input']['Id']
            return input_id
        else:
            return 0


def destination_url():
    client = boto3.client('medialive',region_name='ap-south-1')
    mediapackage = []
    response = client.list_channels(
        MaxResults=123,

    )
    for i in response['Channels']:
        mediapackage.append(i['Destinations'][0]['Settings'][0]['Url'])

    return mediapackage


def return_des_url():
    mediapackage = destination_url()
    client = boto3.client('mediapackage',region_name='ap-south-1')
    response = client.list_channels(
        MaxResults=12,

    )
    for i in response['Channels']:
        count = 0
        for j in (i['HlsIngest']['IngestEndpoints']):

            if (j['Url'] not in mediapackage):
                count += 1
                if count == 2:
                    url = i['HlsIngest']['IngestEndpoints'][0]
                    return url
                else:
                    continue
    return 0


def youtube_info():
    youtube_out = {

        "OutputGroupSettings": {
            "RtmpGroupSettings": {
                "AuthenticationScheme": "COMMON",
                "CacheLength": 30,
                "RestartDelay": 15,
                "CacheFullBehavior": "DISCONNECT_IMMEDIATELY",
                "CaptionData": "ALL",
                "InputLossAction": "PAUSE_OUTPUT",

            }
        },
        "Name": "YouTube Live",
        "Outputs": [
            {
                "OutputSettings": {
                    "RtmpOutputSettings": {
                        "Destination": {
                            "DestinationRefId": "f8vjy7"
                        },
                        "ConnectionRetryInterval": 2,
                        "NumRetries": 10,
                        "CertificateMode": "VERIFY_AUTHENTICITY"
                    }
                },
                "OutputName": "YouTube-Destination",
                "VideoDescriptionName": "video_cjnm1i",
                "AudioDescriptionNames": [
                    "audio_jbdwwv"
                ],
                "CaptionDescriptionNames": [

                ]
            }
        ]
    }
    youtube_audio = {
        "CodecSettings": {
            "AacSettings": {
                "Profile": "LC",
                "InputType": "NORMAL",
                "RateControlMode": "CBR",
                "Spec": "MPEG4",
                "SampleRate": 44100,
                "Bitrate": 128000,
                "CodingMode": "CODING_MODE_2_0",
                "RawFormat": "NONE"
            }
        },
        "LanguageCodeControl": "FOLLOW_INPUT",
        "AudioTypeControl": "FOLLOW_INPUT",
        "Name": "audio_jbdwwv",
        "AudioSelectorName": "Default"
    }
    youtube_video = {
        "CodecSettings": {
            "H264Settings": {
                "Syntax": "DEFAULT",
                "Profile": "MAIN",
                "GopSize": 1,
                "AfdSignaling": "NONE",
                "FramerateControl": "INITIALIZE_FROM_SOURCE",
                "ColorMetadata": "INSERT",
                "FlickerAq": "ENABLED",
                "LookAheadRateControl": "MEDIUM",
                "Bitrate": 400000,
                "TimecodeInsertion": "PIC_TIMING_SEI",
                "NumRefFrames": 1,
                "EntropyEncoding": "CABAC",
                "GopSizeUnits": "SECONDS",
                "Level": "H264_LEVEL_AUTO",
                "GopBReference": "DISABLED",
                "AdaptiveQuantization": "MEDIUM",
                "GopNumBFrames": 0,
                "ScanType": "PROGRESSIVE",
                "ParControl": "INITIALIZE_FROM_SOURCE",
                "SpatialAq": "ENABLED",
                "TemporalAq": "ENABLED",
                "RateControlMode": "CBR",
                "SceneChangeDetect": "ENABLED",
                "GopClosedCadence": 1
            }
        },
        "Name": "video_cjnm1i",
        "Sharpness": 50,
        "Height": 540,
        "Width": 360,
        "ScalingBehavior": "DEFAULT",
        "RespondToAfd": "NONE"
    }
    return youtube_out, youtube_video, youtube_audio


def facebook_info():
    facebook_out = {
        "OutputGroupSettings": {
            "RtmpGroupSettings": {
                "AuthenticationScheme": "COMMON",
                "CacheLength": 30,
                "RestartDelay": 15,
                "CacheFullBehavior": "DISCONNECT_IMMEDIATELY",
                "CaptionData": "ALL",
                "InputLossAction": "PAUSE_OUTPUT",

            }
        },
        "Name": "Facebook",
        "Outputs": [
            {
                "OutputSettings": {
                    "RtmpOutputSettings": {
                        "Destination": {
                            "DestinationRefId": "25x9d"
                        },
                        "ConnectionRetryInterval": 2,
                        "NumRetries": 10,
                        "CertificateMode": "VERIFY_AUTHENTICITY"
                    }
                },
                "OutputName": "Facebook-Destination",
                "VideoDescriptionName": "video_79cd4",
                "AudioDescriptionNames": [
                    "audio_l6ku4t"
                ],
                "CaptionDescriptionNames": []
            }
        ]
    }
    facebook_audio = {
        "CodecSettings": {
            "AacSettings": {
                "Profile": "LC",
                "InputType": "NORMAL",
                "RateControlMode": "CBR",
                "Spec": "MPEG4",
                "SampleRate": 44100,
                "Bitrate": 128000,
                "CodingMode": "CODING_MODE_2_0",
                "RawFormat": "NONE"
            }
        },
        "LanguageCodeControl": "FOLLOW_INPUT",
        "AudioTypeControl": "FOLLOW_INPUT",
        "Name": "audio_l6ku4t",
        "AudioSelectorName": "audio_l6ku4t"
    }
    facebook_video = {
        "CodecSettings": {
            "H264Settings": {
                "Syntax": "DEFAULT",
                "Profile": "MAIN",
                "GopSize": 1,
                "AfdSignaling": "NONE",
                "FramerateControl": "INITIALIZE_FROM_SOURCE",
                "ColorMetadata": "INSERT",
                "FlickerAq": "ENABLED",
                "LookAheadRateControl": "MEDIUM",
                "Bitrate": 400000,
                "TimecodeInsertion": "PIC_TIMING_SEI",
                "NumRefFrames": 1,
                "EntropyEncoding": "CABAC",
                "GopSizeUnits": "SECONDS",
                "Level": "H264_LEVEL_AUTO",
                "GopBReference": "DISABLED",
                "AdaptiveQuantization": "MEDIUM",
                "GopNumBFrames": 0,
                "ScanType": "PROGRESSIVE",
                "ParControl": "INITIALIZE_FROM_SOURCE",
                "SpatialAq": "ENABLED",
                "TemporalAq": "ENABLED",
                "RateControlMode": "CBR",
                "SceneChangeDetect": "ENABLED",
                "GopClosedCadence": 1
            }
        },
        "Name": "video_79cd4",
        "Sharpness": 50,
        "Height": 540,
        "Width": 360,
        "ScalingBehavior": "DEFAULT",
        "RespondToAfd": "NONE"
    }
    return facebook_out, facebook_video, facebook_audio


def runningstatus(channel_id):
    client = boto3.client('medialive',region_name='ap-south-1')
    for i in range(1, 1000):
        sta = client.describe_channel(
            ChannelId=channel_id
        )
        val = sta['State']
        if sta['State'] == 'RUNNING':
            val = sta['State']
            return val




def both_create_channel(client, Destination, input_attachment, arn, ID, facebook, youtube):
    facebook_out, facebook_video, facebook_audio = facebook_info()

    youtube_out, youtube_video, youtube_audio = youtube_info()
    response = client.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=Destination,
        InputAttachments=input_attachment,
        EncoderSettings={
            "TimecodeConfig": {
                "Source": "EMBEDDED"
            },
            "OutputGroups": [
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "fhj9nv",
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 3,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 2,
                            "ProgramDateTimePeriod": 2,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            },
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [
                                "ELEMENTAL_SCTE35"
                            ],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "Mode": "LIVE"
                        }
                    },
                    "Outputs": [
                        {
                            "VideoDescriptionName": "video_1080p30",
                            "AudioDescriptionNames": [
                                "audio_1"
                            ],
                            "CaptionDescriptionNames": [],
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "NameModifier": "_1080p30",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "Media Package"
                },
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "3tzfia"
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 7,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 1,
                            "ProgramDateTimePeriod": 1,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "Mode": "VOD",
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            }
                        }
                    },
                    "Outputs": [
                        {
                            "OutputName": "vf6z8",
                            "AudioDescriptionNames": [
                                "audio_f42hdc"
                            ],
                            "CaptionDescriptionNames": [],
                            "VideoDescriptionName": "video_tikzx7",
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "SegmentModifier": "$dt$",
                                    "NameModifier": "_1",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "NO_PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "S3"
                },
                facebook_out,
                youtube_out,

            ],
            "GlobalConfiguration": {
                "SupportLowFramerateInputs": "DISABLED",
                "OutputTimingSource": "SYSTEM_CLOCK",
                "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
            },
            "CaptionDescriptions": [],
            "VideoDescriptions": [
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",

                            "Profile": "MAIN",
                            "GopSize": 2,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "HIGH",

                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",

                            "NumRefFrames": 3,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "ENABLED",
                            "AdaptiveQuantization": "HIGH",
                            "GopNumBFrames": 2,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "Slices": 1,
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_1080p30",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",
                            "Profile": "MAIN",
                            "GopSize": 1,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "MEDIUM",
                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",
                            "NumRefFrames": 1,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "DISABLED",
                            "AdaptiveQuantization": "MEDIUM",
                            "GopNumBFrames": 0,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_tikzx7",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                facebook_video,
                youtube_video

            ],
            "AudioDescriptions": [
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCode": "eng",
                    "AudioSelectorName": "Default",
                    "LanguageCodeControl": "USE_CONFIGURED",
                    "AudioTypeControl": "USE_CONFIGURED",
                    "AudioType": "UNDEFINED",
                    "Name": "audio_1"
                },
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCodeControl": "FOLLOW_INPUT",
                    "AudioTypeControl": "FOLLOW_INPUT",
                    "Name": "audio_f42hdc",
                    "AudioSelectorName": "Default"
                },
                facebook_audio,
                youtube_audio
            ]
        },
        InputSpecification={
            'Codec': 'AVC',
            'MaximumBitrate': 'MAX_10_MBPS',
            'Resolution': 'SD'
        },
        Name=ID,

        RoleArn=arn)
    return response


def facebook_create_channel(client, Destination, input_attachment, arn, ID, facebook):
    facebook_out, facebook_video, facebook_audio = facebook_info()
    response = client.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=Destination,
        InputAttachments=input_attachment,
        EncoderSettings={
            "TimecodeConfig": {
                "Source": "EMBEDDED"
            },
            "OutputGroups": [
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "fhj9nv",
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 3,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 2,
                            "ProgramDateTimePeriod": 2,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            },
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [
                                "ELEMENTAL_SCTE35"
                            ],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "Mode": "LIVE"
                        }
                    },
                    "Outputs": [
                        {
                            "VideoDescriptionName": "video_1080p30",
                            "AudioDescriptionNames": [
                                "audio_1"
                            ],
                            "CaptionDescriptionNames": [],
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "NameModifier": "_1080p30",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "Media Package"
                },
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "3tzfia"
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 7,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 1,
                            "ProgramDateTimePeriod": 1,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "Mode": "VOD",
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            }
                        }
                    },
                    "Outputs": [
                        {
                            "OutputName": "vf6z8",
                            "AudioDescriptionNames": [
                                "audio_f42hdc"
                            ],
                            "CaptionDescriptionNames": [],
                            "VideoDescriptionName": "video_tikzx7",
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "SegmentModifier": "$dt$",
                                    "NameModifier": "_1",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "NO_PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "S3"
                },
                facebook_out,

            ],
            "GlobalConfiguration": {
                "SupportLowFramerateInputs": "DISABLED",
                "OutputTimingSource": "SYSTEM_CLOCK",
                "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
            },
            "CaptionDescriptions": [],
            "VideoDescriptions": [
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",

                            "Profile": "MAIN",
                            "GopSize": 2,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "HIGH",

                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",

                            "NumRefFrames": 3,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "ENABLED",
                            "AdaptiveQuantization": "HIGH",
                            "GopNumBFrames": 2,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "Slices": 1,
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_1080p30",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",
                            "Profile": "MAIN",
                            "GopSize": 1,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "MEDIUM",
                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",
                            "NumRefFrames": 1,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "DISABLED",
                            "AdaptiveQuantization": "MEDIUM",
                            "GopNumBFrames": 0,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_tikzx7",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                facebook_video,

            ],
            "AudioDescriptions": [
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCode": "eng",
                    "AudioSelectorName": "Default",
                    "LanguageCodeControl": "USE_CONFIGURED",
                    "AudioTypeControl": "USE_CONFIGURED",
                    "AudioType": "UNDEFINED",
                    "Name": "audio_1"
                },
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCodeControl": "FOLLOW_INPUT",
                    "AudioTypeControl": "FOLLOW_INPUT",
                    "Name": "audio_f42hdc",
                    "AudioSelectorName": "Default"
                },
                facebook_audio,
            ]
        },
        InputSpecification={
            'Codec': 'AVC',
            'MaximumBitrate': 'MAX_10_MBPS',
            'Resolution': 'SD'
        },
        Name=ID,

        RoleArn=arn)
    return response


def youtube_create_channel(client, Destination, input_attachment, arn, ID, youtube):
    youtube_out, youtube_video, youtube_audio = youtube_info()
    response = client.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=Destination,
        InputAttachments=input_attachment,
        EncoderSettings={
            "TimecodeConfig": {
                "Source": "EMBEDDED"
            },
            "OutputGroups": [
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "fhj9nv",
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 3,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 2,
                            "ProgramDateTimePeriod": 2,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            },
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [
                                "ELEMENTAL_SCTE35"
                            ],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "Mode": "LIVE"
                        }
                    },
                    "Outputs": [
                        {
                            "VideoDescriptionName": "video_1080p30",
                            "AudioDescriptionNames": [
                                "audio_1"
                            ],
                            "CaptionDescriptionNames": [],
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "NameModifier": "_1080p30",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "Media Package"
                },
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "3tzfia"
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 7,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 1,
                            "ProgramDateTimePeriod": 1,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "Mode": "VOD",
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            }
                        }
                    },
                    "Outputs": [
                        {
                            "OutputName": "vf6z8",
                            "AudioDescriptionNames": [
                                "audio_f42hdc"
                            ],
                            "CaptionDescriptionNames": [],
                            "VideoDescriptionName": "video_tikzx7",
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "SegmentModifier": "$dt$",
                                    "NameModifier": "_1",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "NO_PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "S3"
                },
                youtube_out,

            ],
            "GlobalConfiguration": {
                "SupportLowFramerateInputs": "DISABLED",
                "OutputTimingSource": "SYSTEM_CLOCK",
                "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
            },
            "CaptionDescriptions": [],
            "VideoDescriptions": [
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",

                            "Profile": "MAIN",
                            "GopSize": 2,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "HIGH",

                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",

                            "NumRefFrames": 3,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "ENABLED",
                            "AdaptiveQuantization": "HIGH",
                            "GopNumBFrames": 2,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "Slices": 1,
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_1080p30",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",
                            "Profile": "MAIN",
                            "GopSize": 1,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "MEDIUM",
                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",
                            "NumRefFrames": 1,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "DISABLED",
                            "AdaptiveQuantization": "MEDIUM",
                            "GopNumBFrames": 0,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_tikzx7",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                youtube_video,

            ],
            "AudioDescriptions": [
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCode": "eng",
                    "AudioSelectorName": "Default",
                    "LanguageCodeControl": "USE_CONFIGURED",
                    "AudioTypeControl": "USE_CONFIGURED",
                    "AudioType": "UNDEFINED",
                    "Name": "audio_1"
                },
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCodeControl": "FOLLOW_INPUT",
                    "AudioTypeControl": "FOLLOW_INPUT",
                    "Name": "audio_f42hdc",
                    "AudioSelectorName": "Default"
                },
                youtube_audio,
            ]
        },
        InputSpecification={
            'Codec': 'AVC',
            'MaximumBitrate': 'MAX_10_MBPS',
            'Resolution': 'SD'
        },
        Name=ID,

        RoleArn=arn)
    return response


def create_channel(client, Destination, input_attachment, arn, ID):
    response = client.create_channel(
        ChannelClass='SINGLE_PIPELINE',
        Destinations=Destination,
        InputAttachments=input_attachment,
        EncoderSettings={
            "TimecodeConfig": {
                "Source": "EMBEDDED"
            },
            "OutputGroups": [
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "fhj9nv",
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 3,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 2,
                            "ProgramDateTimePeriod": 2,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            },
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [
                                "ELEMENTAL_SCTE35"
                            ],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "Mode": "LIVE"
                        }
                    },
                    "Outputs": [
                        {
                            "VideoDescriptionName": "video_1080p30",
                            "AudioDescriptionNames": [
                                "audio_1"
                            ],
                            "CaptionDescriptionNames": [],
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "NameModifier": "_1080p30",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "Media Package"
                },
                {
                    "OutputGroupSettings": {
                        "HlsGroupSettings": {
                            "TimedMetadataId3Frame": "PRIV",
                            "CaptionLanguageMappings": [],
                            "Destination": {
                                "DestinationRefId": "3tzfia"
                            },
                            "IvSource": "FOLLOWS_SEGMENT_NUMBER",
                            "IndexNSegments": 7,
                            "InputLossAction": "PAUSE_OUTPUT",
                            "ManifestDurationFormat": "FLOATING_POINT",
                            "CodecSpecification": "RFC_4281",
                            "IvInManifest": "INCLUDE",
                            "TimedMetadataId3Period": 1,
                            "ProgramDateTimePeriod": 1,
                            "SegmentLength": 2,
                            "CaptionLanguageSetting": "OMIT",
                            "ProgramDateTime": "INCLUDE",
                            "Mode": "VOD",
                            "TsFileMode": "SEGMENTED_FILES",
                            "StreamInfResolution": "INCLUDE",
                            "ClientCache": "ENABLED",
                            "AdMarkers": [],
                            "KeepSegments": 7,
                            "SegmentationMode": "USE_SEGMENT_DURATION",
                            "OutputSelection": "MANIFESTS_AND_SEGMENTS",
                            "ManifestCompression": "NONE",
                            "DirectoryStructure": "SINGLE_DIRECTORY",
                            "HlsCdnSettings": {
                                "HlsBasicPutSettings": {
                                    "ConnectionRetryInterval": 1,
                                    "FilecacheDuration": 300,
                                    "NumRetries": 10
                                }
                            }
                        }
                    },
                    "Outputs": [
                        {
                            "OutputName": "vf6z8",
                            "AudioDescriptionNames": [
                                "audio_f42hdc"
                            ],
                            "CaptionDescriptionNames": [],
                            "VideoDescriptionName": "video_tikzx7",
                            "OutputSettings": {
                                "HlsOutputSettings": {
                                    "SegmentModifier": "$dt$",
                                    "NameModifier": "_1",
                                    "HlsSettings": {
                                        "StandardHlsSettings": {
                                            "M3u8Settings": {
                                                "PcrControl": "PCR_EVERY_PES_PACKET",
                                                "TimedMetadataBehavior": "NO_PASSTHROUGH",
                                                "PmtPid": "480",
                                                "Scte35Pid": "500",
                                                "VideoPid": "481",
                                                "ProgramNum": 1,
                                                "AudioPids": "492-498",
                                                "AudioFramesPerPes": 4,
                                                "EcmPid": "8182",
                                                "Scte35Behavior": "NO_PASSTHROUGH"
                                            },
                                            "AudioRenditionSets": "PROGRAM_AUDIO"
                                        }
                                    }
                                }
                            }
                        }
                    ],
                    "Name": "S3"
                },

            ],
            "GlobalConfiguration": {
                "SupportLowFramerateInputs": "DISABLED",
                "OutputTimingSource": "SYSTEM_CLOCK",
                "InputEndAction": "SWITCH_AND_LOOP_INPUTS"
            },
            "CaptionDescriptions": [],
            "VideoDescriptions": [
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",

                            "Profile": "MAIN",
                            "GopSize": 2,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "HIGH",

                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",

                            "NumRefFrames": 3,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "ENABLED",
                            "AdaptiveQuantization": "HIGH",
                            "GopNumBFrames": 2,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "Slices": 1,
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_1080p30",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },
                {
                    "CodecSettings": {
                        "H264Settings": {
                            "Syntax": "DEFAULT",
                            "Profile": "MAIN",
                            "GopSize": 1,
                            "AfdSignaling": "NONE",
                            "FramerateControl": "INITIALIZE_FROM_SOURCE",
                            "ColorMetadata": "INSERT",
                            "FlickerAq": "ENABLED",
                            "LookAheadRateControl": "MEDIUM",
                            "Bitrate": 400000,
                            "TimecodeInsertion": "PIC_TIMING_SEI",
                            "NumRefFrames": 1,
                            "EntropyEncoding": "CABAC",
                            "GopSizeUnits": "SECONDS",
                            "Level": "H264_LEVEL_AUTO",
                            "GopBReference": "DISABLED",
                            "AdaptiveQuantization": "MEDIUM",
                            "GopNumBFrames": 0,
                            "ScanType": "PROGRESSIVE",
                            "ParControl": "INITIALIZE_FROM_SOURCE",
                            "SpatialAq": "ENABLED",
                            "TemporalAq": "ENABLED",
                            "RateControlMode": "CBR",
                            "SceneChangeDetect": "ENABLED",
                            "GopClosedCadence": 1
                        }
                    },
                    "Name": "video_tikzx7",
                    "Sharpness": 50,
                    "Height": 540,
                    "Width": 360,
                    "ScalingBehavior": "DEFAULT",
                    "RespondToAfd": "NONE"
                },

            ],
            "AudioDescriptions": [
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCode": "eng",
                    "AudioSelectorName": "Default",
                    "LanguageCodeControl": "USE_CONFIGURED",
                    "AudioTypeControl": "USE_CONFIGURED",
                    "AudioType": "UNDEFINED",
                    "Name": "audio_1"
                },
                {
                    "CodecSettings": {
                        "AacSettings": {
                            "Profile": "LC",
                            "InputType": "NORMAL",
                            "RateControlMode": "CBR",
                            "Spec": "MPEG4",
                            "SampleRate": 44100,
                            "Bitrate": 128000,
                            "CodingMode": "CODING_MODE_2_0",
                            "RawFormat": "NONE"
                        }
                    },
                    "LanguageCodeControl": "FOLLOW_INPUT",
                    "AudioTypeControl": "FOLLOW_INPUT",
                    "Name": "audio_f42hdc",
                    "AudioSelectorName": "Default"
                },

            ]
        },
        InputSpecification={
            'Codec': 'AVC',
            'MaximumBitrate': 'MAX_10_MBPS',
            'Resolution': 'SD'
        },
        Name=ID,

        RoleArn=arn)
    return response
def return_cloudfornt(cloudfornt_val):
    cloudfront = [{
        "mediapackage": "https://b4fccfcab3a283c8.mediapackage.ap-south-1.amazonaws.com/in/v2/ab30cbb2037245f4be0a7d54898ede1b/ab30cbb2037245f4be0a7d54898ede1b/channel",
        "cloudfront": "https://d25i7g6ykuwpaw.cloudfront.net/out/v1/cfc0ec0a4d8d4cfea2403e4e3c3305a0/index.m3u8"
    },
        {
            "mediapackage": "https://8dc923984a2db229.mediapackage.ap-south-1.amazonaws.com/in/v2/2b0ea8b6e0fb4c2887947734d0b01163/2b0ea8b6e0fb4c2887947734d0b01163/channel",
            "cloudfront": "https://d227d6pfshqvdr.cloudfront.net/out/v1/4257bd00c107426baa3af63232cfd732/index.m3u8"

        },
        {
            "mediapackage": "https://b4fccfcab3a283c8.mediapackage.ap-south-1.amazonaws.com/in/v2/62534cfcc04346939f18521b99c7c78b/62534cfcc04346939f18521b99c7c78b/channel",
            "cloudfront": "https://ds4250e4a8pxq.cloudfront.net/out/v1/e71e8ac1a8124099b6dfffc4aeff1bf9/index.m3u8"

        },
        {
            "mediapackage": "https://b4fccfcab3a283c8.mediapackage.ap-south-1.amazonaws.com/in/v2/acdd061788814a489492c1a7e5678d0a/acdd061788814a489492c1a7e5678d0a/channel",
            "cloudfront": "https://dq61c2oi9wyba.cloudfront.net/out/v1/283f6ec4b7a5450785342ee9984c69bc/index.m3u8"

        },
        {
            "mediapackage": "https://8dc923984a2db229.mediapackage.ap-south-1.amazonaws.com/in/v2/09f3c0b540ab424290f0a64de2e99f81/09f3c0b540ab424290f0a64de2e99f81/channel",
            "cloudfront": "https://d3jci102c00w9v.cloudfront.net/out/v1/34895252d3bd4c1fa9dec65a01961760/index.m3u8"
        }
    ]
    string = cloudfornt_val
    for i in cloudfront:
        if string == i['mediapackage']:
            url = i['cloudfront']
            break
    return url


class medialive(APIView):
    def post(self, request, *args, **kwargs):
        try:
            client = boto3.client('medialive',region_name='ap-south-1')
            merchant_id = request.data.get("merchantid",None)
            merchant_id = re.sub(r'[\!\*\(\)\;\:\@\&\=\+\$\,\/\?\%\#\[\] ]', '_', merchant_id)
            live_id = request.data.get("liveid",None)
            live_id = re.sub(r'[\!\*\(\)\;\:\@\&\=\+\$\,\/\?\%\#\[\] ]', '_', live_id)
            live_name = request.data.get("livename",None)
            live_name = re.sub(r'[\!\*\(\)\;\:\@\&\=\+\$\,\/\?\%\#\[\] ]', '_', live_name)
            facebook = request.data.get("facebook",None)
            youtube = request.data.get("youtube",None)
            facebook_url = request.data.get("facebookurl",None)
            facebook_stream = request.data.get("facebookstream",None)
            youtube_url=request.data.get("youtubeurl",None)
            youtube_stream = request.data.get("youtubestream",None)
            emergency = request.data.get("emergency",None)
            input = request.data.get("input",None)
            if input == 'start':
                if merchant_id and live_id and live_name:
                    Input_id = inputId(merchant_id, live_name, live_id)
                    if Input_id:
                        response = client.describe_input(
                            InputId='{}'.format(Input_id)
                        )
                        Input_url = response['Destinations']
                        return_destination_url = return_des_url()
                        cloud_front=return_cloudfornt(return_destination_url['Url'])

                        if return_destination_url:
                            input_attachment = [{
                                "InputId": "{}".format(Input_id),
                                "InputSettings": {
                                    "AudioSelectors": [],
                                    "CaptionSelectors": [{
                                        "Name": "{}".format(live_name),
                                        "SelectorSettings": {
                                            "EmbeddedSourceSettings": {
                                                "Convert608To708": "DISABLED",
                                                "Scte20Detection": "OFF",
                                                "Source608ChannelNumber": 1,
                                                "Source608TrackNumber": 1
                                            }
                                        }
                                    }],
                                    "DeblockFilter": "DISABLED",
                                    "DenoiseFilter": "DISABLED",
                                    "FilterStrength": 1,
                                    "InputFilter": "AUTO",
                                    "NetworkInputSettings": {
                                        "ServerValidation": "CHECK_CRYPTOGRAPHY_AND_VALIDATE_NAME"
                                    },
                                    "SourceEndBehavior": "CONTINUE"
                                }
                            }]
                            arn = 'arn:aws:iam::563076992460:role/MediaLiveAccessRole'
                            ID = "{}_{}".format(merchant_id, live_id)
                            Destination = [
                                {
                                    'Id': 'fhj9nv',
                                    'MediaPackageSettings': [],
                                    'Settings': [
                                        {
                                            # 'StreamName': 'string',
                                            "Url": return_destination_url['Url'],
                                            "Username": return_destination_url['Username'],
                                            "PasswordParam": "/medialive/MediaLive_channel2_mumbai_password"
                                        },
                                    ]
                                },
                                {
                                    "Id": "3tzfia",
                                    "Settings": [
                                        {
                                            "Url": "https://ad-live-streaming.s3-ap-southeast-1.amazonaws.com/live_show/{}/{}/{}".format(
                                                merchant_id, live_id, live_name)
                                        }
                                    ],
                                    "MediaPackageSettings": []
                                },
                            ]
                            if facebook and youtube:
                                if facebook_url and facebook_stream and youtube_url and youtube_stream:
                                    facebookurl = {
                                        "Id": "25x9d",
                                        "Settings": [
                                            {
                                                "Url": facebook_url,
                                                "StreamName": facebook_stream
                                            }
                                        ],
                                        "MediaPackageSettings": []
                                    }
                                    Destination.append(facebookurl)
                                    youtubeurl = {
                                        "Id": "f8vjy7",
                                        "Settings": [
                                            {
                                                "Url": youtube_url,
                                                "StreamName": youtube_stream
                                            }
                                        ],
                                        "MediaPackageSettings": []
                                    }
                                    Destination.append(youtubeurl)
                                    repo = both_create_channel(client, Destination, input_attachment, arn, ID, youtube,
                                                               facebook)
                                else:
                                    return Response({"msg": "something is wrong with facebook and youtube url input"})

                            elif facebook:
                                if facebook_url and facebook_stream:
                                    facebookurl = {
                                        "Id": "25x9d",
                                        "Settings": [
                                            {
                                                "Url": facebook_url,
                                                "StreamName": facebook_stream
                                            }
                                        ],
                                        "MediaPackageSettings": []
                                    }
                                    Destination.append(facebookurl)
                                    repo = facebook_create_channel(client, Destination, input_attachment, arn, ID,
                                                                   facebook)
                                else:
                                    return Response({"msg": "something is wrong with facebook  url input"})

                            elif youtube:
                                if youtube_stream and youtube_url:
                                    youtubeurl = {
                                        "Id": "f8vjy7",
                                        "Settings": [
                                            {
                                                "Url": youtube_url,
                                                "StreamName": youtube_stream
                                            }
                                        ],
                                        "MediaPackageSettings": []
                                    }
                                    Destination.append(youtubeurl)
                                    repo = youtube_create_channel(client, Destination, input_attachment, arn, ID,
                                                                  youtube)
                                else:
                                    return Response({"msg": "something is wrong with youtube  url input"})

                            else:
                                repo = create_channel(client, Destination, input_attachment, arn, ID)

                            channel_no = repo['Channel']['Id']
                            time.sleep(6)
                            stopedstatus(channel_no)

                            client.start_channel(
                                ChannelId=channel_no
                            )
                            time.sleep(30)
                            value = runningstatus(channel_no)

                            if value == 'RUNNING':
                                url = "https://ad-live-streaming.s3-ap-southeast-1.amazonaws.com/live_show/{}/{}/{}.m3u8".format(
                                    merchant_id, live_id, live_name)
                                return Response ({'status': True, "inputurl": Input_url, "cloudfront":cloud_front, 'msg': 'Channel Started Successfully',
                                     'archiveurl': url,'channelid':channel_no})

                        else:
                            client.delete_input(
                                InputId=Input_id
                            )
                            return Response({"msg": "Channel all are booked please wait for  Channel free"})

                    else:
                        return Response({"msg": "Channel all are booked please wait for  Channel free"})
                else:
                    return Response({"msg": "something is wrong with input"})
            elif input == 'stop':
                channelid = request.data.get("channelid")
                if channelid:
                    val="State"
                    status=getstatus(val,channelid)
                    if (status == 'IDLE') or (status == 'RUNNING'):
                        client = boto3.client('medialive',region_name='ap-south-1')
                        client.stop_channel(
                            ChannelId=channelid
                        )
                        time.sleep(40)
                        value = stopedstatus(channelid)
                        if value == 'IDLE':
                            url = "" + geturl(channelid) + ".m3u8"
                            response = client.delete_channel(
                                ChannelId=channelid
                            )
                            inputid=response['InputAttachments'][0]['InputId']
                            time.sleep(5)
                            client.delete_input(
                                InputId=inputid
                            )
                            return Response({'status': True, 'msg': 'Channel Stoped Successfully', 'archiveurl': url})
                    else:
                        if status == 'STOPPING':
                            value = stopedstatus(channelid)
                            if (value == 'IDLE') or (value == 'RUNNING'):
                                client.stop_channel(
                                    ChannelId=channelid
                                )
                                return Response({'status': True, 'msg': 'Channel Stoped Successfully'})
                        return Response({'status': False, 'msg': 'Channel ' + status + ' Please wait for IDLE state'})

                else:
                    return Response({"msg": "something is wrong with input"})
            elif emergency:
                ID= "{}_{}".format(merchant_id,live_id)
                value = emergency_stop(ID)
                if value:
                    status = stopedstatus(value)

                    if (status == 'IDLE') or (status == 'RUNNING'):
                        client.stop_channel(
                            ChannelId=value
                        )
                        response = client.delete_channel(
                            ChannelId=value
                        )
                        inputid = response['InputAttachments'][0]['InputId']
                        time.sleep(5)
                        client.delete_input(
                            InputId=inputid
                        )
                        return Response({'status': True, 'msg': 'Channel Stoped Successfully'})
                    return Response({"msg": "something is wrong with input"})

                return Response({"msg": "something is wrong with input"})

            else:
                return Response({"msg": "something is wrong with input"})

        except Exception as e:
            print(e)
            return Response({"msg": "something is wrong"})

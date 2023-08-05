

AOS_ANIMATIONS = ['fade',
                    'fade-up',
                    'fade-down',
                    'fade-left',
                    'fade-right',
                    'fade-up-right',
                    'fade-up-left',
                    'fade-down-right',
                    'fade-down-left',
                    'flip-up',
                    'flip-down',
                    'flip-left',
                    'flip-right',
                    'slide-up',
                    'slide-down',
                    'slide-left',
                    'slide-right',
                    'zoom-in',
                    'zoom-in-up',
                    'zoom-in-down',
                    'zoom-in-left',
                    'zoom-in-right',
                    'zoom-out',
                    'zoom-out-up',
                    'zoom-out-down',
                    'zoom-out-left',
                    'zoom-out-right',
                    ]


AOS_ANCHOR_PLACEMENT = [None,
                        'top-bottom',
                        'top-center',
                        'top-top',
                        'center-bottom',
                        'center-center',
                        'center-top',
                        'bottom-bottom',
                        'bottom-center',
                        'bottom-top',
                        ]



AOS_EASING = [None,
              'linear',
                'ease',
                'ease-in',
                'ease-out',
                'ease-in-out',
                'ease-in-back',
                'ease-out-back',
                'ease-in-out-back',
                'ease-in-sine',
                'ease-out-sine',
                'ease-in-out-sine',
                'ease-in-quad',
                'ease-out-quad',
                'ease-in-out-quad',
                'ease-in-cubic',
                'ease-out-cubic',
                'ease-in-out-cubic',
                'ease-in-quart',
                'ease-out-quart',
                'ease-in-out-quart',
                ]

AOS_ANIMATIONS = ((a, a) for a in AOS_ANIMATIONS)
AOS_ANCHOR_PLACEMENT = ((a, a) for a in AOS_ANCHOR_PLACEMENT)
AOS_EASING = ((a, a) for a in AOS_EASING)
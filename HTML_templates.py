CHAT_REF =  '<a class="chat_ref__outer" href="/chat/{0}">' \
                '<div class="chat_ref__outer">' \
                    '<div class="chat_ref__inner">' \
                        '<div class="chat_ref_avatar">' \
                            '<icon><img class="icon" src="/static/gallery/icons/profile.png" width="100%"></icon>' \
                        '</div>' \
                        '<div class="chat_ref_name">{1}</div>' \
                    '</div>' \
                '</div>' \
            '</a>'

RTL_MESSAGE =   '<div class="message_RTL">' \
                    '<div class="message__outer">' \
                        '<div class="message__avatar">' \
                        '</div>' \
                        '<div class="message__inner">' \
                            '<div class="message__bubble__blue">' \
                                '<span>{0}</span>' \
                            '</div>' \
                            '<div class="message__actions">' \
                            '</div>' \
                            '<div class="message__spacer"></div>' \
                        '</div>' \
                        '<div class="message__status">' \
                        '</div>' \
                    '</div>' \
                '</div>'

LTL_MESSAGE =   '<div class="message_LTL">' \
                    '<div class="message__outer">' \
                        '<div class="message__inner">' \
                            '<div class="message__spacer"></div>' \
                            '<div class="message__actions">' \
                            '</div>' \
                            '<div class="message__bubble__grey">' \
                                '<span>{0}</span>' \
                            '</div>' \
                        '</div>' \
                        '<div class="message__avatar">' \
                        '</div>' \
                    '</div>' \
                '</div>'

FRIEND_REF =    '<a class="friends_list_ref__outer" href="/user/name={0}">' \
                    '<div class="friends_list_ref__outer">' \
                        '<div class="friends_list_ref__inner">' \
                            '<div class="universal_spacer"></div>' \
                            '<div class="friends_list_ref__bubble">' \
                                '<div class="chat_ref_avatar">' \
                                    '<icon>' \
                                        '<img class="icon" src="/static/gallery/icons/profile.png" width="100%">' \
                                    '</icon>' \
                                '</div>' \
                                '<div class="chat_ref_name">' \
                                    '{1}' \
                                '</div>' \
                            '</div>' \
                            '<div class="universal_spacer"></div>' \
                        '</div>' \
                    '</div>' \
                '</a>'

FRIEND_REF_CHAT =   '<a class="friends_list_ref__outer" href="/newchat/{0}">' \
                        '<div class="friends_list_ref__outer">' \
                            '<div class="friends_list_ref__inner">' \
                                '<div class="universal_spacer"></div>' \
                                '<div class="friends_list_ref__bubble">' \
                                    '<div class="chat_ref_avatar">' \
                                        '<icon>' \
                                            '<img class="icon" src="/static/gallery/icons/profile.png" width="100%">' \
                                        '</icon>' \
                                    '</div>' \
                                    '<div class="chat_ref_name">' \
                                        '{1}' \
                                    '</div>' \
                                '</div>' \
                                '<div class="universal_spacer"></div>' \
                            '</div>' \
                        '</div>' \
                    '</a>'

POST =  '<a class="post" href="/watch/post={0}">' \
            '<div class="post">' \
                '<div class="post__outer">' \
                    '<div class="post__inner">' \
                        '<div class="post__sender__outer">' \
                            '<div class="post__sender__inner">' \
                                '<div class="post__sender__bubble">' \
                                    '<div class="post__sender">' \
                                        '<span>{1}</span>' \
                                    '</div>' \
                                    '<div class="universal_spacer"></div>' \
                                    '<div class="post__time">' \
                                        '<span>{2}</span>' \
                                    '</div>' \
                                    '<div class="vertical_line"></div>' \
                                    '<div class="post__date">' \
                                        '<span>{3}</span>' \
                                    '</div>' \
                                '</div>' \
                            '</div>' \
                        '</div>' \
                        '<div class="universal_spacer"></div>' \
                        '<div class="post__body__outer">' \
                            '<div class="post__body__inner">' \
                                '<div class="post__body__bubble">' \
                                    '<span>{4}</span>' \
                                '</div>' \
                            '</div>' \
                        '</div>' \
                        '<div class="universal_spacer"></div>' \
                        '<div class="post__footer__outer">' \
                            '<div class="post__footer__inner">' \
                                '<div class="post__footer__bubble">' \
                                    '<div class="post__views__outer">' \
                                        '<div class="post__views__inner">' \
                                            '<icon><img src="/static/gallery/icons/views.png" width="100%">' \
                                            '</icon>' \
                                            '<div class="post__views__text">' \
                                                '<span>{5}</span>' \
                                            '</div>' \
                                        '</div>' \
                                    '</div>' \
                                    '<div class="universal_spacer"></div>' \
                                    '<div class="post__commentaries__outer">' \
                                        '<div class="post__commentaries__inner">' \
                                            '<div class="post__commentaries__text">' \
                                                '<span>1k</span>' \
                                            '</div>' \
                                            '<icon><img src="/static/gallery/icons/commentaries.png" width="100%"></icon>' \
                                        '</div>' \
                                    '</div>' \
                                '</div>' \
                            '</div>' \
                        '</div>' \
                    '</div>' \
                '</div>' \
            '</div>' \
        '</a>'

POST_WITHOUT_REF =  '<div class="post">' \
                        '<div class="post__outer">' \
                            '<div class="post__inner">' \
                                '<div class="post__sender__outer">' \
                                    '<div class="post__sender__inner">' \
                                        '<div class="post__sender__bubble">' \
                                            '<div class="post__sender">' \
                                                '<span>{1}</span>' \
                                            '</div>' \
                                            '<div class="universal_spacer"></div>' \
                                            '<div class="post__time">' \
                                                '<span>{2}</span>' \
                                            '</div>' \
                                            '<div class="vertical_line"></div>' \
                                            '<div class="post__date">' \
                                                '<span>{3}</span>' \
                                            '</div>' \
                                        '</div>' \
                                    '</div>' \
                                '</div>' \
                                '<div class="universal_spacer"></div>' \
                                '<div class="post__body__outer">' \
                                    '<div class="post__body__inner">' \
                                        '<div class="post__body__bubble">' \
                                            '<span>{4}</span>' \
                                        '</div>' \
                                    '</div>' \
                                '</div>' \
                                '<div class="universal_spacer"></div>' \
                                '<div class="post__footer__outer">' \
                                    '<div class="post__footer__inner">' \
                                        '<div class="post__footer__bubble">' \
                                            '<div class="post__views__outer">' \
                                                '<div class="post__views__inner">' \
                                                    '<icon><img src="/static/gallery/icons/views.png" width="100%">' \
                                                    '</icon>' \
                                                    '<div class="post__views__text">' \
                                                        '<span>{5}</span>' \
                                                    '</div>' \
                                                '</div>' \
                                            '</div>' \
                                            '<div class="universal_spacer"></div>' \
                                            '<div class="post__commentaries__outer">' \
                                                '<div class="post__commentaries__inner">' \
                                                    '<div class="post__commentaries__text">' \
                                                        '<span>1k</span>' \
                                                    '</div>' \
                                                    '<icon><img src="/static/gallery/icons/commentaries.png" width="100%"></icon>' \
                                                '</div>' \
                                            '</div>' \
                                        '</div>' \
                                    '</div>' \
                                '</div>' \
                                '<div class="new_commentary__outer">' \
                                    '<div class="new_commentary__inner">' \
                                    '</div>' \
                                '</div>' \
                            '</div>' \
                        '</div>' \
                    '</div>'

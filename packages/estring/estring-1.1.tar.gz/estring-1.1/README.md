
# estring
>__javascript style APIs for string__


# install
>__pip3 install estring__


## QUICK
---------

        BASIC_PY_LESSONS# eses_emoji_strict te
        < telephone >
        < tent >
        < teacup_without_handle >
        < ten_o_clock >
        < ten_thirty >
        < tennis >
        < teddy_bear >
        < telephone_receiver >
        < television >
        < tear_off_calendar >
        < test_tube >
        < telescope >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_strict telephone
        ☎
        < telephone_receiver >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_strict telescope
        🔭
        BASIC_PY_LESSONS#

        BASIC_PY_LESSONS# eses_emoji_loose sneezing
        < cowboy_hat_face_sneezing_face_0 >
        < cowboy_hat_face_sneezing_face_1 >
        < cowboy_hat_face_sneezing_face_2 >
        < cowboy_hat_face_sneezing_face_3 >
        < cowboy_hat_face_sneezing_face_4 >
        < cowboy_hat_face_sneezing_face_5 >
        < cowboy_hat_face_sneezing_face_6 >
        < cowboy_hat_face_sneezing_face_7 >
        < sneezing_face >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_loose cowboy_hat_face_sneezing_face_3
        🤣
        BASIC_PY_LESSONS# eses_emoji_loose cowboy_hat_face_sneezing_face_4
        🤤
        BASIC_PY_LESSONS# eses_emoji_loose cowboy_hat_face_sneezing_face_5
        🤥
        BASIC_PY_LESSONS#

### FORMATTED  EMOJI  RESOURCES
    
    #this original  txt file is from 
    #http://unicode.org/Public/emoji/12.0/
    
[emoji.csv](https://raw.githubusercontent.com/ihgazni2/estring/master/estring/emoji/resources/emoji.csv)<br>
[emoji.dtb.json](https://raw.githubusercontent.com/ihgazni2/estring/master/estring/emoji/resources/emoji.dtb.json)<br>
[emoji.cls.json](https://raw.githubusercontent.com/ihgazni2/estring/master/estring/emoji/resources/emoji.cls.json)<br>
[emoji.sqlite.db](https://github.com/ihgazni2/estring/blob/master/estring/emoji/resources/emoji.sqlite.db?raw=true)<br>


## SPECIAL CHARS APIs
-----------------------------------------------------------------------

### EMOJI API

        from estring.emoji.emoji  import emoji
        >>> emoji.te
        emoji.teacup_without_handle  emoji.telephone              emoji.television             emoji.tennis
        emoji.tear_off_calendar      emoji.telephone_receiver     emoji.ten_o_clock            emoji.tent
        emoji.teddy_bear             emoji.telescope              emoji.ten_thirty             emoji.test_tube
        >>> emoji.teacup_without_handle
        '🍵'
        >>>



### H5 ENTITY

        from estring.h5entity import h5
        >>> h5.theta
        'θ'
        >>> h5.the
        h5.there4     h5.therefore  h5.theta      h5.thetasym   h5.thetav
        >>> h5.theta
        'θ'
        >>> h5.The
        h5.Therefore  h5.Theta
        >>> h5.Theta
        'Θ'
        >>>




## javascript style string APIs
-----------------------------------------------------------------------
>├──0. [length\<0\>](estring/Images/length.0.png)  <br>
├──0. [length\<1\>](estring/Images/length.1.png)  <br>
├──1. [fromCharCode](estring/Images/fromCharCode.0.png)  <br>
├──2. [fromCodePoint](estring/Images/fromCodePoint.0.png)  <br>
├──3. [charAt\<1\>](estring/Images/charAt.0.png)  <br>
├──3. [charAt\<2\>](estring/Images/charAt.1.png)  <br>
├──4. [charCodeAt\<1\>](estring/Images/charCodeAt.0.png)  <br>
├──4. [charCodeAt\<2\>](estring/Images/charCodeAt.1.png)  <br>
├──5. [codePointAt\<1\>](estring/Images/codePointAt.0.png)  <br>
├──5. [codePointAt\<2\>](estring/Images/codePointAt.1.png)  <br>
├──6. [concat](estring/Images/concat.0.png)  <br>
├──7. [endsWith](estring/Images/endsWith.0.png)  <br>
├──8. [includes](estring/Images/includes.0.png)  <br>
├──9. [indexOf](estring/Images/indexOf.0.png)  <br>
├──10. [padEnd](estring/Images/padEnd.0.png)  <br>
├──11. [padStart](estring/Images/padStart.0.png)  <br>
├──12. [repeat](estring/Images/repeat.0.png)  <br>
├──13. [replace](estring/Images/replace.0.png)  <br>
├──13. [replace](estring/Images/replace.1.png)  <br>
├──13. [replace](estring/Images/replace.2.png)  <br>
├──13. [replace](estring/Images/replace.3.png)  <br>
├──14. [slice\<0\>](estring/Images/slice.0.png)  <br>
├──14. [slice\<1\>](estring/Images/slice.1.png)  <br>
├──15. [split](estring/Images/split.0.png)  <br>
├──15. [search_gen](estring/Images/search_gen.0.png)  <br>
├──15. [find_all_spans](estring/Images/find_all_spans.0.png)  <br>
├──15. [regex_divide](estring/Images/regex_divide.0.png)  <br>
├──16. [startsWith](estring/Images/startsWith.0.png)  <br>
├──17. [substr](estring/Images/substr.0.png)  <br>
├──18. [substring](estring/Images/substring.0.png)  <br>
├──19. [toLowerCase](estring/Images/toLowerCase.0.png)  <br>
├──20. [toUpperCase](estring/Images/toUpperCase.0.png)  <br>
├──21. [trim](estring/Images/trim.0.png)  <br>
├──22. [trimLeft](estring/Images/trimLeft.0.png)  <br>
├──23. [trimRight](estring/Images/trimRight.0.png)  <br>
├──. [](estring/Images/.0.png)  <br>

-----------------------------------------------------------------------


## supplementary APIs
-----------------------------------------------------------------------
>├──0. [divide](estring/Images/divide.0.png)  <br>
├──1. [indexesAll](estring/Images/indexesAll.0.png)  <br>
├──2. [strip](estring/Images/strip.0.png)  <br>
├──3. [lstrip](estring/Images/lstrip.0.png)  <br>
├──4. [rstrip](estring/Images/rstrip.0.png)  <br>
├──5. [reverse](estring/Images/reverse.0.png)  <br>
├──6. [prepend](estring/Images/prepend.0.png)  <br>
├──7. [append](estring/Images/append.0.png)  <br>
├──8. [xor](estring/Images/xor.0.png)  <br>
├──9. [tail2head](estring/Images/tail2head.0.png)  <br>
├──10. [end2begin](estring/Images/tail2head.0.png)  <br>
├──11. [head2tail](estring/Images/head2tail.0.png)  <br>
├──12. [begin2end](estring/Images/head2tail.0.png)  <br>
├──13. [display_width](estring/Images/.0.png)  <br>
├──14. [prepend_basedon_displaywidth](estring/Images/prepend_basedon_displaywidth.0.png)  <br>
├──15. [append_basedon_displaywidth](estring/Images/append_basedon_displaywidth.0.png)  <br>
├──16. [](estring/Images/.0.png)  <br>
├──17. [](estring/Images/.0.png)  <br>
-----------------------------------------------------------------------



-----------------------------------------------------------------------


## IO APIs
-----------------------------------------------------------------------
>├──0. [str2io](estring/Images/str2io.0.png)  <br>
├──1. [](estring/Images/.0.png)  <br>
-----------------------------------------------------------------------





-----------------------------------------------------------------------

## encode decode APIs
-----------------------------------------------------------------------
>├──0. [get_bominfo](estring/Images/get_bominfo.0.png)  <br>
├──1. [remove_bom](estring/Images/remove_bom.0.png)  <br>
├──2. [get_bomtype\<1\>](estring/Images/get_bomtype.0.png)  <br>
├──3. [get_bomtype\<2\>](estring/Images/get_bomtype.1.png)  <br>
├──4. [decode_chbyts](estring/Images/decode_chbyts.0.png)  <br>
├──4. [byts2chstr](estring/Images/decode_chbyts.0.png)  <br>
├──4. [unpack_chbyts](estring/Images/decode_chbyts.0.png)  <br>
├──5. [pack_chstr](estring/Images/pack_chstr.0.png)  <br>
├──5. [chstr2byts](estring/Images/pack_chstr.0.png)  <br>
├──5. [encode_chstr](estring/Images/pack_chstr.0.png)  <br>
├──6. [pack_chnum](estring/Images/pack_chnum.0.png)  <br>
├──6. [chnum2byts](estring/Images/pack_chnum.0.png)  <br>
├──6. [encode_chnum](estring/Images/pack_chnum.0.png)  <br>
├──7. [byts2chnum](estring/Images/byts2chnum.0.png)  <br>
├──8. [decode_bytstrm](estring/Images/decode_bytstrm.0.png)  <br>
├──8. [bytstrm2str](estring/Images/decode_bytstrm.0.png)  <br>
├──8. [unpack_bytstrm](estring/Images/decode_bytstrm.0.png)  <br>
├──9. [pack_str](estring/Images/packstr.0.png)  <br>
├──9. [encode_str](estring/Images/packstr.0.png)  <br>
├──9. [str2bytstrm](estring/Images/packstr.0.png)  <br>
├──10. [slash_show](estring/Images/slash_show.0.png)  <br>
├──11. [bytstrm2hex](estring/Images/bytstrm2hex.0.png)  <br>
├──12. [hex2bytstrm](estring/Images/hex2bytstrm.0.png)  <br>
├──13. [strm2bytnums](estring/Images/strm2bytnums.0.png)  <br>
├──14. [bytnums2strm](estring/Images/bytnums2strm.0.png)  <br>
├──15. [bytstrm2chnums](estring/Images/bytstrm2chnums.0.png)  <br>
├──16. [strm2chnums](estring/Images/bytstrm2chnums.0.png)  <br>
├──17. [chnums2bytstrm](estring/Images/chnums2bytstrm.0.png)  <br>
├──18. [chnums2strm](estring/Images/chnums2bytstrm.0.png)  <br>
├──19. [bytstrm2us\<1\>](estring/Images/bytstrm2us.0.png)  <br>
├──19. [bytstrm2us\<2\>](estring/Images/bytstrm2us.1.png)  <br>
├──20. [us2bytstrm\<1\>](estring/Images/us2bytstrm.0.png)  <br>
├──21. [us2bytstrm\<2\>](estring/Images/us2bytstrm.1.png)  <br>
├──22. [us2bytstrm\<3\>](estring/Images/us2bytstrm.2.png)  <br>
├──23. [str2hex](estring/Images/str2hex.0.png)  <br>
├──24. [hex2str](estring/Images/hex2str.0.png)  <br>
├──25. [str2chnums](estring/Images/str2chnums.0.png)  <br>
├──26. [chnums2str](estring/Images/chnums2str.0.png)  <br>
├──27. [str2bytnums](estring/Images/str2bytnums.0.png)  <br>
├──28. [bytnums2str](estring/Images/bytnums2str.0.png)  <br>
├──29. [str2us](estring/Images/str2us.0.png)  <br>
├──30. [us2str](estring/Images/us2str.0.png)  <br>
├──31. [hex2bytnums](estring/Images/hex2bytnums.0.png)  <br>
├──32. [bytnums2hex](estring/Images/bytnums2hex.0.png)  <br>
├──33. [hex2chnums](estring/Images/hex2chnums.0.png)  <br>
├──34. [chnums2hex](estring/Images/chnums2hex.0.png)  <br>
├──35. [hex2us](estring/Images/hex2us.0.png)  <br>
├──36. [us2hex](estring/Images/us2hex.0.png)  <br>
├──37. [chnums2bytnums](estring/Images/chnums2bytnums.0.png)  <br>
├──38. [bytnums2chnums](estring/Images/bytnums2chnums.0.png)  <br>
├──39. [chnums2us](estring/Images/chnums2us.0.png)  <br>
├──40. [us2chnums](estring/Images/us2chnums.0.png)  <br>
├──41. [bytnums2us](estring/Images/bytnums2us.0.png)  <br>
├──42. [us2bytnums](estring/Images/us2bytnums.0.png)  <br>
├──43. [str_code_points\<0\>](estring/Images/str_code_points.0.png)  <br>
├──44. [str_code_points\<1\>](estring/Images/str_code_points.1.png)  <br>
├──45. [str_jschar_points](estring/Images/str_jschar_points.0.png)  <br>
├──46. [pychpoints2jscharpoints](estring/Images/pychpoints2jscharpoints.0.png)  <br>
├──47. [jscharpoints2pychpoints](estring/Images/jscharpoints2pychpoints.0.png)  <br>
├──48. [us2uarr](estring/Images/us2uarr.0.png)  <br>
├──49. [uarr2us](estring/Images/uarr2us.0.png)  <br>
├──50. [uarr2jscharr](estring/Images/uarr2jscharr.0.png)  <br>
├──51. [uarr2str](estring/Images/uarr2str.0.png)  <br>
├──52. [str2uarr](estring/Images/str2uarr.0.png)  <br>
├──53. [str2jscharr](estring/Images/str2jscharr.0.png)  <br>
├──54. [camel2dash](estring/Images/.0.png)  <br>
├──55. [camel2lod](estring/Images/.0.png)  <br>
├──56. [capinit](estring/Images/.0.png)  <br>
├──57. [dash2camel](estring/Images/.0.png)  <br>
├──58. [dash2lod](estring/Images/.0.png)  <br>
├──59. [lod2camel](estring/Images/.0.png)  <br>
├──60. [lod2dash](estring/Images/.0.png)  <br>
├──61. [is_int_str](estring/Images/.0.png)  <br>
├──62. [is_float_str](estring/Images/.0.png)  <br>




## CLI
-----------------------------------------------------------------------
* eses_camel2dash   
* eses_camel2lod    
* eses_capinit      
* eses_dash2camel   
* eses_dash2lod     
* eses_lod2camel    
* eses_lod2dash 


        estring# eses_camel2dash   acceptCharset
        accept-charset
        estring# eses_camel2lod    acceptCharset
        accept_charset
        estring# eses_capinit      accept
        Accept
        estring# eses_dash2camel   accept-charset
        acceptCharset
        estring# eses_dash2lod     accept-charset
        accept_charset
        estring# eses_lod2camel    accept_charset
        acceptCharset
        estring# eses_lod2dash     accept_charset
        accept-charset


* eses_h5entity_strict

        ESTRING# eses_h5entity_strict theta
        θ
        < thetasym >
        < thetav >
        ESTRING#
        ESTRING# eses_h5entity_strict the
        < there4 >
        < therefore >
        < theta >
        < thetasym >
        < thetav >
        ESTRING#
        ESTRING# eses_h5entity_strict theta
        θ
        < thetasym >
        < thetav >
        ESTRING#
        ESTRING# eses_h5entity_strict alph
        < alpha >
        ESTRING#
        ESTRING# eses_h5entity_strict alpha
        α
        ESTRING#

*eses_h5entity_loose

        ESTRING# eses_h5entity_loose Op
        < OpenCurlyDoubleQuote >
        < OpenCurlyQuote >
        ESTRING#
        ESTRING# eses_h5entity_loose OpenCurlyDoubleQuote
        “
        ESTRING#

*eses_emoji_strict

        BASIC_PY_LESSONS# eses_emoji_strict te
        < telephone >
        < tent >
        < teacup_without_handle >
        < ten_o_clock >
        < ten_thirty >
        < tennis >
        < teddy_bear >
        < telephone_receiver >
        < television >
        < tear_off_calendar >
        < test_tube >
        < telescope >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_strict telephone
        ☎
        < telephone_receiver >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_strict telescope
        🔭
        BASIC_PY_LESSONS#


*eses_emoji_loose

        BASIC_PY_LESSONS# eses_emoji_loose gon
        < mahjong_red_dragon >
        < dragon_face >
        < dragon >
        < mahjong_tile_red_dragon >
        BASIC_PY_LESSONS#
        BASIC_PY_LESSONS# eses_emoji_strict mahjong_red_dragon
        🀄
        BASIC_PY_LESSONS#


-----------------------------------------------------------------------


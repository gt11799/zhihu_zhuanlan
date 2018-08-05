签名规则
===

>时间仓促，签名只支持GET接口

## 签名概述

签名的设计主要基于三部分

- 防止重放。使用了时间戳放在了header里，调试期间超时时间是2000s，上线会改为20s
- 防止篡改参数。把请求的参数和时间戳作为message做签名
- 防止伪造。用了一个secret key。客户端需妥善保管(作为单独的打包参数，不要放在git中，本地文件里尽量加密保存)

签名所需要的算法

- 排序算法。按照字母顺序(英文字母和数字在不同的语言中基本一致)
- 哈希算法。本算法使用的是`SHA1`算法
- hmac算法。也是哈希算法的一种，支持密钥

## 签名过程

- 把要请求的参数，加上当前的时间戳(integer, 单位是秒，java出来的是毫秒，需要转换)，组成一个字典(map), 时间戳的key是`ts`
 - 比如要请求的参数是`{"last_id": 1, "month": 2}`
 - 增加ts后，变成`{"last_id": 1, "month": 2, "ts": 1533461609}`
- 把字典按照key排序, 然后按照`key=value&key=value`拼接起来
 - 字典一般是无序的，通常需要转换为列表(数组)
 - 在Python中，一般排序后转换为列表套元组(不可变数组)的形式。`[('last_id', 1), ('month', 2), 'ts': 1533461609]`
 - 上述排序好的列表，再组装起来，得到字符串`last_id=12&month=1&ts=1533461609`
- 把字符串当做message，加上secret_key作为key，算法使用hmac计算散列值，取16进制的结果(通常方法名类似`hexdigest`)
 - 可以参考[这个网站](https://1024tools.com/hmac), 里面的结果1
 - java直接hmac出来的通常是个二进制数组，所以要找到方法，取出16进制。可以[参考这里](https://stackoverflow.com/questions/3208160/how-to-generate-an-hmac-in-java-equivalent-to-a-python-example)的答案2，`Hex.encodeHexString`
- token需要指定类型，写死`Bearer`，上述得到的token，拼起来就是`Bearer bfc8a6040324391f162a43ebc5694b7c0119b7ad`

## 发出请求

Headers需要额外添加

- Headers中需要放入时间戳(正整数的字符串，单位是秒), key为`X-TS`
- Headers中需要放入token， key是`Authorization`

## 调试接口

联调阶段，只有`/article/images`加了签名

### 签名测试接口

`GET /_internal/sign_test`

参数：联调时随意加，以验证算法

返回

```js
{
    "data": {
        "qs": {  // 请求的参数
            "last_id": "12",
            "month": "1"
        },
        "to_sign_data": {  // 加上了ts的数据
            "last_id": "12",
            "month": "1",
            "ts": "1533461609"
        },
        "to_sign_string": "last_id=12&month=1&ts=1533461609",  // 排序后拼接的字符串
        "token": "Bearer 9889d7778f89bf6e55860fd5960abb7ace553816",  // 服务器端生成的token
        "token_given": "Bearer bfc8a6040324391f162a43ebc5694b7c0119b7ad",  // 传入的token
        "ts": "1533461609"  // 传入的时间戳
    }
}
```

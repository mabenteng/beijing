//随机key,用来随机截取15个字符串
var key="tuD&#mheJQBlgy&Sm300l8xK^X4NzFYBcrN8@YLCret$fv1AZbtujg*KN^$YnUkh"
//返回随机的下标索引1-40  也就是可以截取16-55其中的字符串
var keyindex = Math.floor(40 * Math.random()) + 1
//将oParams对象转为json字符串
sParams = JSON.stringify(oParams)



/*
return {
    key: keyindex,#随机返回一个下标,比如14
    sign: md5("coapi" + sParams + this.key.substr(keyindex, 15)),#生成一个md5用来验证
    params: sParams
}
 */
//ajax请求的真实地址
//https://coapi.51job.com/job_list.php?jsoncallback=jQuery300004316137724455249_1622019039930&key=13&sign=签名&params=字典参数&_=时间戳
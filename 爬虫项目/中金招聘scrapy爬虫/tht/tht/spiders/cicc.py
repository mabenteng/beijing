import scrapy
from tht.items import ThtItem
import redis,re
#引入items字段可以使用小写,前提是到settings中去启动管道,不然不能提示

# 初始化redis连接池     注意目前redis引入需要每次采集一个新项目清空redis,不然可能有bug
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  

'''
# 使用redis分析.目前虽然可以做到采集到28页爬虫断了下次执行还是28页执行,但是这里是有bug会漏采数据
# 原因是scrapy是采用异步IO的方式去采集数据,也就是说分页采集到28页很有可能第20页的的详情页还没有采集完毕
# 如果此时断了爬虫,那么虽然下次从28页开始采集,20-28的列表页是访问了,但是20-28页的详情页的url还没有访问到还在队列中
# 所以下次采集从28页开始,那么20-28页的详情页就没有采集到数据..........

---------------------
2021年5月23日 17:09:59
目前断线可以恢复上次的页码进行读取,但是第一页最少要访问一次,还有就是如果访问第一页就中断,那么redis的分类key就不会生成,访问不是starturls中的链接才会生成

现在有个新问题.校招只有5页,url一个还没有访问,因为scrapy正在忙社招和实习生招聘,但是到尾页校招就访问第一个排序小url更新redis了.

'''

class CiccSpider(scrapy.Spider):
    name = 'cicc' #中金公司
    allowed_domains = ['cicc.zhiye.com']
    #这里start_urls后期可以同时社会招聘   校园招聘   实习生招聘三者并行
    start_urls = ['http://cicc.zhiye.com/szzw']#,'http://cicc.zhiye.com/xzzw','http://cicc.zhiye.com/sxszw']
    base_url="http://cicc.zhiye.com"

    #引入redis用来去重结果
    def getredisinfo(self,urlcode):
        '''根据url判断是否重复'''
        if r.sismember(self.name, urlcode):#存在url说明以前采集过
            return True
        return False
        
    def parse(self, response):
        # 先进行判断状态码
        if response.status==200:
            # print("开始进行解析.")
            nextpage=response.xpath("//a[text()='下一页']/@href").extract_first()
            #nextpage在最后一页是空对象,将其转为""
            nextpage=nextpage if nextpage else ""
            #定义分页page_flag标志,用来保存爬取到第几页了.key为xyzw
            page_flag=re.findall(r'\.com/(\w+)/?',response.url)[0]
            page_flag=self.name+'_'+page_flag
            curpage=response.xpath("//div[@class='zwlb']/div/a[@class='now']/text()").extract_first()
            print(curpage)
            #采集到哪一个分页就保存到redis中方便下次直接跳转到这里.保存详情页分页需要到jobinfourl函数中
            curpageurl=re.sub(r'PageIndex=\d+','PageIndex='+curpage,nextpage) #这里正则要匹配多个数字,不然两位数就报错了
            # print(curpageurl+"------当前列表分页的网页深度是:"+str(response.meta['depth']))
            #此时nextpage还是第一页,下面会变成redis保存的页
            isstarturl=0
            if response.url in self.start_urls:
                #爬虫刚开始访问判断是否存在分页key,存在就直接用他的val,不存在就默认第二页
                isstarturl=1 # 判断如果是第一次访问,就让这个变量为true
                if r.exists(page_flag):
                    nextpage=r.get(page_flag)
                print("我是爬虫刚启动访问的页面,当前页码是"+curpage+"即将访问--------------"+nextpage)
            else:
                #不是第一次访问就保存详情页正在爬的页数,而不是已经访问过的页面
                # 因为第一次访问要判断如果key有值就从这个值开始爬
                # 需要处理curpage为url后缀 re.sub(r'PageIndex=\d','PageIndex=66',a)
                # 将redis设置分页值放到详情页去设置
                # 每次访问详情页都将当前页,当前页url和招聘类型的缩写传入详情页函数用来添加redis
                pass
                
            # 招聘职位的列表
            list_jobs=response.xpath("//div[@class='zwlb']//tr/td[2]/a/@href").extract()
            for onejob in list_jobs:
                #先判断当前的url是否存在,存在就退出
                '''
                # 这里捋一捋     再次启动先访问redis保存的页码(比如第4页),下一页就变成第一页了!!!!
                原因是访问starturls是第一页,上面有个第一页in starturls判断第一次会改变nextpage的值,但是传入的curpage等于nextpage有关系的变量还是第一页的参数
                '''
                if self.getredisinfo(re.findall(r'jobId=(\d+)',onejob)[0]):
                    print("当前页码"+page_flag.split("_")[1]+curpage+'-----当前职位url已经采集过,跳到下一个!'+onejob)
                    #如果当前页所有详情url都存在那么页要更新一下redis
                    #######注意一般可以不开启,适合1-99页都采集过了但是redis还是标记的3页,因为前99页内容都存在所以退出循环不会访问详情页也就不会更新redis了
                    if isstarturl==0:#如果不是刚开始的页就更新下redis
                        #用redis在详情页中去设置招聘类别爬到当前的页码url    
                        r.set(page_flag, curpageurl)
                    continue
                    # 数据全部采集完了,以后要return来只添加新的数据
                    # return "当前职位url已经采集过,退出爬虫!"
                #开始拼凑每一个职位的url进行提交请求
                jobinfourl=self.base_url+onejob
                # print(jobinfourl) #打印下一页的url
                yield scrapy.Request(jobinfourl,callback=self.parseinfo,meta={'curpage':curpage,'curpageurl':curpageurl,"page_flag":page_flag,'isstarturl':isstarturl})
            
            # if nextpage:#有值就可以直接请求到下一页
            #     # print("将要访问这个分页面--------------"+nextpage)
            #     yield scrapy.Request(self.base_url+nextpage,callback=self.parse)

    def parseinfo(self,response):
        '''开始解析招聘的详情页'''
        # 先进行判断状态码
        if response.status==200:
            # print("解析文章正文内容")
            # 这里用meta取值是为了详情页采到哪一页及时保存redis,断线下次直接从这一页开始
            curpage=response.meta['curpage']
            curpageurl=response.meta['curpageurl']
            print(curpageurl+"------当前详情页的网页深度:"+str(response.meta['depth'])+"____________________")
            page_flag=response.meta['page_flag']
            #如果isstarturl是0,说明爬虫不是刚开始执行就添加redis,因为每次都是从starurls中先执行一次
            if response.meta['isstarturl']==0:
                #用redis在详情页中去设置招聘类别爬到当前的页码url    
                r.set(page_flag, curpageurl)
            #data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department']
            # ,data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']
            item=ThtItem()
            item['securities']="中金公司"
            item['title']=response.xpath("//h2[@class='title2 pb10']/text()").extract_first()
            # 直接一步到位将zwxq的class删除
            item['content']=response.xpath("//div[@class='zwxq']").get().replace('class="zwxq"',"")
            item['job_addr']=response.xpath("//li[@class='icon13d']/span/text()").extract_first()
            item['job_category']=response.xpath("//li[@class='icon13a']/span/text()").extract_first()
            item['end_time']=""#结束时间.中金公司没有此字段
            time_elem=response.xpath("//li[@class='icon13c']/span/text()").extract()
            if len(time_elem)==2:#如果有两个元素那么说明有结束时间
                item['end_time']=time_elem[1]
            item['publish_time']=time_elem[0] if time_elem else ''
            item['department']=response.xpath("//li[@class='icon22']/span/text()").extract_first()
            item['job_number']=""#招聘人数.中金公司没有此字段
            item['job_education']=""#学历要求.中金公司没有此字段
            item['others']='' #其他额外需要保存的字段,暂时没有
            item['source_url']=response.url #本页url
            print(item['securities']+"---"+item['job_category']+"---"+curpageurl+"---"+item['source_url'])
            r.sadd(self.name,re.findall(r'jobId=(\d+)',item['source_url'])[0]) #临时禁用sql添加key
            # yield item










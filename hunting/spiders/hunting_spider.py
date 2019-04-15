import scrapy
import itertools


class spSpider(scrapy.Spider):
    name = "hunting"

    def start_requests(self):
        urls = [
            'http://www.huntingseasonhq.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url_state = response.xpath("//p/a/@href").extract()
        for url in url_state:
            self.logger.info("Starting for state: {}".format(" ".join(response.url.split("/")[-2].split("-")[:-2])))
            self.logger.info(url)
            yield scrapy.Request(url=url, callback=self.parse_state)

    def parse_state(self, response):
        state = " ".join(response.url.split("/")[-2].split("-")[:-2])
        animal_list = response.xpath("//p/strong/text()").extract()

        """
        Georgia , Montana special case
        """
        if state == "georgia":
            animal_list = [i for i in animal_list if "\u00a0" not in i]
            animal_list = ["G"+i if "G" not in i else i for i in animal_list]

        if state == "montana":
            animal_list += response.xpath("//p/b/text()").extract()[-1]

        animal_list = list(filter(lambda a: a != "\u00a0", animal_list))
        # pay attention to how to do this
        weapon_date_list = [i.xpath(".//td/text()").extract() for i in response.xpath("//table")]
        animal_list = animal_list[:len(weapon_date_list)]
        len_list = map(lambda x: len(x) // 2, weapon_date_list)
        weapon_date_list = list(itertools.chain(*weapon_date_list))
        animal_list = [[animal] * length for (length, animal) in zip(len_list, animal_list)]
        animal_list = list(itertools.chain(*animal_list))
        weapon_list  = weapon_date_list[::2]
        date_list = weapon_date_list[1::2]

        """"
        this part specially for Hawaii
        """
        if state == "hawaii":
            animal_list = response.xpath("//p/b/text()").extract()
            weapon_date_list = []
            for i in response.xpath("//table"):
                if len(i.xpath(".//td/p/text()").extract()) > 0:
                    weapon_date_list.append(i.xpath(".//td/p/text()").extract())
                else:
                    weapon_date_list.append(i.xpath(".//td/text()").extract())

            animal_list = animal_list[:len(weapon_date_list)]
            len_list = map(lambda x: len(x) // 2, weapon_date_list)
            weapon_date_list = list(itertools.chain(*weapon_date_list))
            animal_list = [[animal] * length for (length, animal) in zip(len_list, animal_list)]
            animal_list = list(itertools.chain(*animal_list))
            weapon_list = weapon_date_list[::2]
            date_list = weapon_date_list[1::2]

        self.logger.info("for {} scraped {} entities".format(state,len(date_list)))
        for i in range(len(date_list)):
            item = {
                    "state": state,
                    "animal": animal_list[i],
                    "weapon": weapon_list[i],
                    "date": date_list[i],
                    }
            yield item

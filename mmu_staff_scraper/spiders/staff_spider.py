import scrapy

from scrapy_splash import SplashRequest

from mmu_staff_scraper.items import MmuStaffScraperItem

class StaffSpider(scrapy.Spider):
    name = "staff_dir"

    def start_requests(self):
        urls = [
            'http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?page=1',
            'http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?page=2',
            'http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?page=3',
            'http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?page=4',
            'http://foe.mmu.edu.my/v3/main/staff/staff_directory.php?method=Name&searchkey=&page=5'
        ]
        for url in urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        staff_names = response.xpath('//*[@id="main"]/table[2]/tbody/tr[position() mod 2 = 0]/th/text()').extract()
        contact_details = response.xpath('//*[@id="main"]/table[2]/tbody/tr[position() mod 2 = 1]/td/center/div/div/div[2]/text()').extract()

        removed_symbols = (' '.join(contact_details)).split('\xa0')
        removed_symbols = list(filter(None, removed_symbols))

        removed_colon = (' '.join(removed_symbols)).split(' : ')
        removed_colon = list(filter(None, removed_colon))

        removed_empty_spaces = (' '.join(removed_colon)).split('  ')
        removed_empty_spaces = list(filter(None, removed_empty_spaces))

        cleaned_contacts = [w.replace('[at]', '@') for w in removed_empty_spaces]

        # n = 3
        # split_cleaned_contacts = [cleaned_contacts[i:i + n] for i in range(0, len(cleaned_contacts), n)]

        items = []
        j = 0
        for i, staff_name in enumerate(staff_names):
            item = MmuStaffScraperItem()

            item['name'] = staff_name

            if 'FOE' in cleaned_contacts[j]:
                item['room_number'] = cleaned_contacts[j]
                j += 1
            else:
                print("break at room number")
                continue

            if '@mmu.edu.my' in cleaned_contacts[j]:
                item['email'] = cleaned_contacts[j]
                j += 1
            else:
                print("break at email")
                continue

            if 'FOE' not in cleaned_contacts[j]:
                item['contact_no'] = cleaned_contacts[j]
                j += 1
            else:
                print("break at contact no")
                continue

            items.append(item)

            yield item








        # details = $x('//*[@id="main"]/table[2]/tbody/tr[1]/td[2]/center/div/div/div[2]/text()')

        # //*[@id="staff_contact"]/text()[2]
        # //*[@id="staff_contact"]/text()[2]
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
from selenium import webdriver as wd
import chromedriver_binary

wd = wd.Chrome()
wd.implicitly_wait(10)

wd.get('https://www.amazon.com/MEROKEETY-Popcorn-Batwing-Cardigan-Oversized/dp/B08C4VFDQC/ref=sr_1_1?keywords=cardigans&pd_rd_r=0d5667f7-cf42-47bc-a293-ac945c57021f&pd_rd_w=n6UEY&pd_rd_wg=nypok&pf_rd_p=bb27b743-d39d-4423-a18e-dd1d61011f4f&pf_rd_r=MVKNQDYWBS7KRXH26QZ9&qid=1644738540&s=fashion-womens-intl-ship&sr=1-1&th=1&psc=1')

add_to_cart_button = wd.find_element_by_xpath('//*[@id="add-to-cart-button"]')

add_to_cart_button.click()
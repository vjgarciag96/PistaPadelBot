from telegram.ext import Updater, CommandHandler
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import datetime
TOKEN = "YOUR_BOT_TOKEN"

MONDAY_CODE = 0
TUESDAY_CODE = 1
WEDNESDAY_CODE = 2
THURSDAY_CODE = 3
FRIDAY_CODE = 4
SATURDAY_CODE = 5
SUNDAY_CODE = 6

updater = Updater(token=TOKEN)
updater.start_polling()
dispatcher = updater.dispatcher

def getNextDayOfWeek(dayCode):
    now = datetime.datetime.now()
    dateFormatted = datetime.date(now.year, now.month, now.day)
    if(dateFormatted.weekday() != dayCode):
        nextDayOfWeek = dateFormatted + datetime.timedelta((((dayCode - dateFormatted.weekday()) + 7) % 7))
    else:
        nextDayOfWeek = dateFormatted
    return nextDayOfWeek

def getDayId(day):
    splitedDate = str(day).split('-', 3)
    dayId = ''
    for elem in splitedDate:
        dayId = dayId + elem
    return dayId

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Bienvenido a PistaPadelBot, aquí podrás consultar la disponibilidad de pistas de padel de Safyde de la Unex")

def monday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Disponibilidad de pistas para "+str(getNextDayOfWeek(MONDAY_CODE)))
    if(getAvailabilityByDayOfWeek(MONDAY_CODE) == 0):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open("screenshot.png", 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="No es posible reservar pista ese dia todavia. Recuerda que solo puedes reservar dias de la misma semana")

def tuesday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Disponibilidad de pistas para "+str(getNextDayOfWeek(TUESDAY_CODE)))
    if(getAvailabilityByDayOfWeek(TUESDAY_CODE) == 0):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open("screenshot.png", 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="No es posible reservar pista ese dia todavia. Recuerda que solo puedes reservar dias de la misma semana")
def wednesday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Disponibilidad de pistas para "+str(getNextDayOfWeek(WEDNESDAY_CODE)))
    if(getAvailabilityByDayOfWeek(WEDNESDAY_CODE) == 0):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open("screenshot.png", 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="No es posible reservar pista ese dia todavia. Recuerda que solo puedes reservar dias de la misma semana")

def thursday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Disponibilidad de pistas para "+str(getNextDayOfWeek(THURSDAY_CODE)))
    if(getAvailabilityByDayOfWeek(THURSDAY_CODE) == 0):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open("screenshot.png", 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="No es posible reservar pista ese dia todavia. Recuerda que solo puedes reservar dias de la misma semana")

def friday(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Disponibilidad de pistas para "+str(getNextDayOfWeek(FRIDAY_CODE)))
    if(getAvailabilityByDayOfWeek(FRIDAY_CODE) == 0):
        bot.sendPhoto(chat_id=update.message.chat_id, photo=open("screenshot.png", 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="No es posible reservar pista ese dia todavia. Recuerda que solo puedes reservar dias de la misma semana")

def getAvailabilityByDayOfWeek(dayOfWeek):
    available = 0

    url = 'http://reservasid.unex.es/CronosWeb/Login'

    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get(url)
    username = driver.find_element_by_id("ContentSection_txtIdentificador")
    password = driver.find_element_by_id("ContentSection_txtContrasena")

    username.send_keys("your_email")
    password.send_keys("your_password")

    driver.find_element_by_id("ContentSection_lnkEntrar").click()

    driver.find_element_by_xpath('//*[@id="ulOperaciones"]/li[1]/a').click()

    driver.find_element_by_xpath('//*[@id="ulCentros"]/li[2]/a').click()

    #padel manianas
    #driver.find_element_by_xpath('//*[@id="ulActividades"]/li[16]/a').click()
    #padel tardes
    driver.find_element_by_xpath('//*[@id="ulActividades"]/li[17]/a').click()

    date = getNextDayOfWeek(dayOfWeek)
    dateString = ''
    dateString = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
    driver.execute_script("javascript:__doPostBack('Continuar','"+dateString+"');")
    #driver.find_element_by_id('ContentSection_a'+dayOfWeek).click()
    try:
        cuadrante = driver.find_element_by_xpath('//*[@id="tblCuadrante"]/tbody')
        builder = ActionChains(driver)
        builder.move_to_element(cuadrante).perform()
        driver.save_screenshot('screenshot.png')  # saves screenshot of entire page
        driver.close()
    except Exception:
        driver.close()
        available = 1

    return available


def help(bot, update):
	msg = "Escribe uno de estos comandos para hacer funcionar el bot:\n"
	msg += "	- /pistas_lunes: muestra la disponibilidad de pistas del proximo lunes\n"
	msg += "	- /pistas_martes: muestra la disponibilidad de pistas del proximo martes\n"
	msg += "	- /pistas_miercoles: muestra la disponibilidad de pistas del proximo miercoles\n"
	msg += "	- /pistas_jueves: muestra la disponibilidad de pistas del proximo jueves\n"
	msg += "	- /pistas_viernes: muestra la disponibilidad de pistas del proximo viernes\n"
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)

def test(bot, update):
    print "-------------Test Method-------------"
    print "-------------End of Test Method-------------"




dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('pistas_lunes', monday))
dispatcher.add_handler(CommandHandler('pistas_martes', tuesday))
dispatcher.add_handler(CommandHandler('pistas_miercoles', wednesday))
dispatcher.add_handler(CommandHandler('pistas_jueves', thursday))
dispatcher.add_handler(CommandHandler('pistas_viernes', friday))
dispatcher.add_handler(CommandHandler('help', help))
#dispatcher.add_handler(CommandHandler('test', test))

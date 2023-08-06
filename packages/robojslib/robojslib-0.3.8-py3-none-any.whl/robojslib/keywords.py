from robojslib import Error
from robojslib import FatalError

class keywords(robojslib):
@keyword('Vanilla click')
    def check(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        driver.execute_script("document.getElementById('"+arg+"').click()")
        if arg is None:
            raise(FatalError(arg, "non cliccabile"))
        else:
            print("selezionato", arg)
    
    @keyword('Vanilla click by query selector')
    def vcbyqs(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        driver.execute_script("document.querySelector('"+arg+"').click()")
        if arg is None:
            raise(FatalError(arg, "non cliccabile"))
        else:
            print("selezionato", arg)

    @keyword('Check title')
    def func(self):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        title = driver.title
        if  "http" not in title:
            print('titolo della pagina:', title )
        else:
            raise(FatalError("errore, verificare titolo pagina"))

    @keyword('Modify url string')
    def modifyurl(self, arg1, arg2):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        url = driver.current_url
        if arg1 in url:
            driver.delete_all_cookies()
            newUrl = url.replace(arg1, arg2)
            driver.get(newUrl)
            print("stringa ", arg1, " sostituita")
        else:
            raise(Error(arg1, " non sostituibile, verificare"))

    @keyword('Vanilla input')
    def gen(self, arg1, arg2):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        driver.execute_script("document.getElementById('"+arg1+"').value = '"+arg2+"'")

    @keyword('Vanilla input by query selector')
    def genqs(self, arg1, arg2):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        driver.execute_script("document.querySelector('"+arg1+"').value = '"+arg2+"'")

    @keyword('Insert phone nr')
    def Nr(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        nr = random.randint(0, 10000000)
        tel = "351" + str(nr)
        print(tel, "numero generato")
        if arg is not None:
            driver.execute_script("document.getElementById('"+arg+"').value = '"+tel+"'")
            print('numero di telefono generato ', tel, 'inserito in ', arg)
        else:
            print("id non valido")
    
    @keyword('Checkbox control')
    def cc(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        check = driver.find_element_by_id(arg).is_selected()
        if check is True:
            print("checkbox gia selezionato")
        else:
            driver.execute_script("document.getElementById('"+arg+"').click()")
            print("selezionato checkbox", arg)
    
    @keyword('Set responsive')
    def tr(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        if arg == "Mobile":
            driver.set_window_size(360,640)
        elif arg == "Tablet":
            driver.set_window_size(768, 1024)
        elif arg is None:
            raise(Error("missing argument"))   

    @keyword('Wait until title contains')
    def slUUc(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        url = driver.current_url
        wait = WebDriverWait(driver, 20)
        action = wait.until(EC.title_contains(arg))
        if action:
            print(arg, "e' contenuto in url")
        else:
           raise(FatalError(arg, "non e' contenuto in url"))
    
    @keyword('Open new tab')
    def ont(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        driver.execute_script("window.open('"+arg+"', '_blank');")

    @keyword('Check if visible and click')
    def cvc(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        elem = driver.find_element_by_id(arg)
        if elem.is_displayed():
            elem.click()
        else:
            print("elemento non visibile", arg)
    
    @keyword('Check if visible and click by class')
    def cvcbc(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        elem = driver.find_elements_by_class_name(arg)
        if elem.is_displayed():
            elem.click()
        else:
            print("elemento non visibile", arg)

    @keyword('Check if visible and click by css selector')
    def cvcbq(self, arg):
        driver = BuiltIn().get_library_instance('SeleniumLibrary')._current_browser()
        elem = driver.find_element_by_css_selector(arg)
        if elem.is_displayed():
            elem.click()
        else:
            print("elemento non visibile", arg)
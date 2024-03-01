import time
import random
import pyautogui
import utilities.ocr as ocr
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
import utilities.imagesearch as imsearch
from model.osrs.osrs_bot import OSRSBot
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from typing import Union
from typing import List


class gotrbot(OSRSBot):

    def __init__(self):
        bot_title = "gotrbot"
        description = "Guardian of the rift bot"
        super().__init__(bot_title=bot_title, description=description)
        api_m = MorgHTTPSocket()
        api_s = StatusSocket()
        self.options = {"hotkey": "f9"}
        # Initialize the running_time attribute
        self.running_time = 1

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_slider_option("crafting_preference", "Elemental (%) Catalytic", -100, 100)

    def handle_slider_option(self, option, value):
        if option == "crafting_preference":
            # Map the slider values (-100 to 100) to the range [0, 1]
            self.crafting_preference = (value + 100) / 200 if value is not None else 0
            crafting_preference_str = f"{int(value)}% Catalytic - {int(100 - value)}% Elemental"
            self.log_msg(f"Crafting Preference: {crafting_preference_str}")
        elif option == "running_time":
            # Handle the running_time option
            self.running_time = value

    def save_options(self, options: dict):
        for option, value in options.items():
            self.handle_slider_option(option, value)

        self.log_msg("Settings saved successfully")
        self.options_set = True

    def main_looptest(self):
        start_time = time.time()
        end_time = start_time + (self.running_time * 60)

        while time.time() < end_time:
            self.catalytic_runecraft()
            exit()
            

            time.sleep(2)
                # Update progress
            progress = (time.time() - start_time) / (end_time - start_time)
            self.update_progress(progress)

        # Finalization steps after the main loop
        self.update_progress(100)
        self.log_msg("Finished.")
        self.stop()

    def main_loop(self):
        start_time = time.time()
        end_time = start_time + (self.running_time * 60)

        while time.time() < end_time:
            print("gameloop start ", time.time())
            try:
                if self.start():  # Pregame start
                    while True:  # game started                        
                        if self.bench():
                            self.log_msg("Main pouchs")
                            self.gamecheckfinish()
                            if self.pouchs():
                                self.log_msg("Main benchnoportal")
                                self.gamecheckfinish()
                                if self.bench2():
                                    self.log_msg("pouchs2")
                                    self.gamecheckfinish()
                                    if self.pouchs2():
                                        self.log_msg("bench3")
                                        if self.bench2():
                                            if self.Stonealtarmain():
                                                continue
                                            else:
                                                self.log_msg("Critical error at Stonealtarmain")
                                                exit()
                                        else:
                                            self.log_msg("Critical error bench continue")
                                            continue
                                    else:
                                        self.log_msg("Critical error pouchs")
                                        exit()
                                else:
                                    self.log_msg("Critical error bench continue")
                                    continue
                            else:
                                self.log_msg("Critical error pouchs")
                                exit()
                        else:
                            self.log_msg("Critical error bench continue")
                            continue
                else:
                    self.log_msg("Critical error at start")
                    exit()

            except CustomErrorClass as e:
                self.log_msg(e)
                print("game exception caught smelly ", time.time())
                continue

            except CustomErrorClassportal as e:
                self.log_msg(e)
                print("game exception portal ", time.time())
                continue

        # Update progress
        progress = (time.time() - start_time) / (end_time - start_time)
        self.update_progress(progress)

        # Finalization steps after the main loop
        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()

    #all Start and End Logic

    def start(self, api_m=MorgHTTPSocket()): # Local fuctions Called: handle_climbdown, guardian_fragments
        if not self.handle_climbdown(api_m):
            return

        for _ in range(30):
            self.log_msg("start into guardian frag")
            red_click = self.mouse.click(check_red_click=True)
            if red_click:
                self.guardian_fragments()
                return True
            
            else:
                self.log_msg("Can't click after moving to rock (red_click after moving to rock)")
                time.sleep(1)
                return False
        else:
            self.log_msg("Game check failed.")

    def gamecheckstart(self, api_m=MorgHTTPSocket(), max_retries=190, retry_interval=1): # Local fuctions Called: none
        for _ in range(max_retries):
            gamestart = self.chatbox_textred("active!")
            if gamestart:
                self.log_msg("Game started")
                return True
            else:
                self.log_msg("Game not started. Retrying...")
                time.sleep(retry_interval)
        else:
            self.log_msg("Game not started after retries.")
            return False        
  
    def handle_starting_spot(self, api_m=MorgHTTPSocket()): # Local fuctions Called: none
        startingspot = self.get_nearest_tag(clr.BLACKish)
        if startingspot:
            self.mouse.move_to(startingspot.random_point())
            self.mouse.click()
            for _ in range(20):
                idle = api_m.get_is_player_idle()
                if idle:
                    self.log_msg("Cant find starting spot BLACK")
                    return True
                else:
                    self.log_msg("not idle retying")
                    time.sleep(1)

        else:
            self.log_msg("Cant find starting spot BLACK")
            time.sleep(1)
            return False

    def handle_climbdown(self, api_m=MorgHTTPSocket()):
        climbdown = self.get_nearest_tag(clr.WHITE)
        self.log_msg("Climbdown")

        if not climbdown:
            self.log_msg("Climbdown not found")
            time.sleep(1)
            return False

        self.mouse.move_to(climbdown.random_point())
        red_click = self.mouse.click(check_red_click=True)

        if not red_click:
            self.log_msg("Can't click on climbdown (red_click on climbdown)")
            return False

        if not self.is_player_idle3():
            self.log_msg("Player not idle")
            return False

        rock = self.get_nearest_tag(clr.CYAN)

        if not rock:
            self.log_msg("Can't get Cyan")
            return False

        self.mouse.move_to(rock.random_point())
        red_click_rock = self.mouse.click(check_red_click=True)

        if not red_click_rock:
            self.log_msg("Red click fail rock")
            return False

        if not self.gamecheckstart():
            self.log_msg("Can't find gamestart, closing")
            return False
        rock2 = self.get_nearest_tag(clr.CYAN)
        self.log_msg("Let's go!")
        self.mouse.move_to(rock2.random_point())
        return True

    #all Altar Rune and stone Logic

    def altar(self, api_s = StatusSocket(), api_m = MorgHTTPSocket()): # Local fuctions Called: pouchs, droptalismans
        while True:
            altar = self.get_nearest_tag(clr.PINK)
            self.log_msg("Searching for altar1")

            if altar:
                self.log_msg("Found altar")
                self.mouse.move_to(altar.random_point())
                self.log_msg("altar start")
                self.mouse.click()
                self.log_msg("runecrafting")

                for _ in range(10):  # Retry if not idle up to 10 times
                    api_m.wait_til_gained_xp(skill="Runecraft", timeout=10)
                    self.log_msg("idle detected1")
                    emptypouch = self.pouchsaltar()
                    self.log_msg("at emptying pouch")
                    if emptypouch:
                        self.log_msg("Searching for altar2")
                        altar = self.get_nearest_tag(clr.PINK)
                        if altar:
                            self.mouse.move_to(altar.random_point())
                            self.log_msg("Clicking altar")
                            self.mouse.click(button="left")
                            self.log_msg("waiting for RC xp")
                            if api_m.wait_til_gained_xp(skill="Runecraft", timeout=10):
                                emptypouch2 = self.pouchsaltar2()
                                if emptypouch2:
                                    self.log_msg("Searching for altar2")
                                    altar2 = self.get_nearest_tag(clr.PINK)
                                    if altar2:
                                        self.mouse.move_to(altar2.random_point())
                                        self.log_msg("Clicking altar")
                                        self.mouse.click(button="left")
                                        self.log_msg("waiting for RC xp")
                                        if api_m.wait_til_gained_xp(skill="Runecraft", timeout=10):
                                            time.sleep(random.uniform(0.15, 0.3))
                                            self.droptalismans()
                                            time.sleep(random.uniform(0.15, 0.3))
                                            Exit = self.get_nearest_tag(clr.BLUE)
                                            self.mouse.move_to(Exit.random_point())
                                            red_click = self.mouse.click(check_red_click=True)
                                            if red_click:
                                                self.log_msg("Clicked exit")
                                                for _ in range(10):  # Retry if not idle up to 10 times
                                                    idle2 = api_m.get_is_player_idle()
                                                    if idle2:
                                                        self.log_msg("Idle detected2")
                                                        self.log_msg("returning from altar logic")
                                                        return True
                                                    else:
                                                        self.log_msg("idle2 retrying")
                                                        time.sleep(1)  # Wait before retrying
                                                else:
                                                    return False


                                            else:
                                                self.log_msg("Can't find exit retrying")
                                                Exit = self.get_nearest_tag(clr.BLUE)
                                                self.mouse.move_to(Exit.random_point())
                                                red_click = self.mouse.click(check_red_click=True)
                                                if red_click:
                                                    return  True

                                                else:
                                                    return False
                                        else:
                                            self.log_msg("altarissue: api exp 2")
                                            return False        
                                    else:
                                        self.log_msg("altarissue: altar2")
                                        return False      
                                else:
                                    self.log_msg("altarissue: emptypouch2")
                                    return False 
                            else:
                                self.log_msg("altarissue: api exp")
                                return False
                        else:
                            self.log_msg("Can't find altar")
                            return False
                    else:
                        self.log_msg("Can't empty pouch, check empty_pouch")
                        return False
            else:
                self.log_msg("Altar not found, retrying")
                time.sleep(0.5)
                continue

    def Stonealtarmain(self, api_s = StatusSocket(), api_m = MorgHTTPSocket()): # Local fuctions Called: guardian_stones, altar, find_guardian_stones, deposit_runes
        while True:
            self.log_msg("Stonealtarmain: guardian_stones")
            if self.guardian_stones():
                self.log_msg("Stonealtarmain: altar")
                if self.altar():
                    self.log_msg("Stonealtarmain: find_guardian_stones")
                    if self.find_guardian_stones():
                        self.log_msg("Stonealtarmain: deposit_runes")
                        if self.deposit_runes():
                            if self.arerunesgone():
                                self.log_msg("Stonealtarmain: pouchcheck")
                                if self.pouchcheck():
                                    return True
                                else:
                                    self.log_msg("got frags going altar")
                                    continue   
                            else:
                                self.log_msg("Stonealtarmain arerunesgone issue")
                                return False                       
                        else:
                            self.log_msg("Stonealtarmain deposit_runes issue")
                            return False
                    else:
                        self.log_msg("Stonealtarmain find_guardian_stones issue")
                        return False
                else:
                    self.log_msg("Stonealtarmain altar issue")
                    return False
            else:
                self.log_msg("guardian_stones issue")
                return False

    def find_guardian_stones(self, api_s = StatusSocket(), api_m = MorgHTTPSocket()): # Local fuctions Called: dude_guy
        self.log_msg("Attempting to send stones")
        catalytic = api_m.get_first_occurrence(26880)
        elemental = api_m.get_first_occurrence(26881)

        def send_stones(type_name):
            if self.dude_guy():
                if api_m.wait_til_gained_xp(skill="Runecraft", timeout=10):
                    self.log_msg(f"Sent {type_name} stones into portal_loop")
                    if  self.portallogic():
                        return True

                    return True
                
            else:
                self.log_msg(f"Has {type_name} stones but failed at dude guy")
                if self.find_guardian_stones():
                    return True
                else:
                    self.log_msg(f"Has {type_name} stones but failed at dude guy again")
                    return False


        if catalytic:
            return send_stones("catalytic")
            

        if elemental:
            return send_stones("elemental")

        self.log_msg("No stones found")
        return False
        
    def dude_guy(self): # Local fuctions Called: none
        guardian_stone_tag = self.get_nearest_tag(clr.purpleish)
        
        if guardian_stone_tag:
            self.mouse.move_to(guardian_stone_tag.random_point())
            if self.mouse.click(check_red_click=True):
                self.log_msg("Found dude")
                return True
            else:
                self.log_msg("Can't find dude")
        
        return False

    def deposit_runes(self, max_color_retries=5, api_m = MorgHTTPSocket(), api_s = StatusSocket()):  # Add a parameter for the maximum color search retries
        if self.pouchcheck():
            time.sleep(random.uniform(0.2, 0.5))
            self.log_msg("deposit_runes")
            api_m = MorgHTTPSocket()
            api_s = StatusSocket()
            runes = api_m.get_first_occurrence([554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565])

            if runes:
                self.log_msg("deposit_runes get_first_occurrence")
                color_retries = 0

                while color_retries < max_color_retries:
                    self.log_msg("deposit_runes get clr.ORANGE")
                    deposit = self.get_nearest_tag(clr.ORANGE)

                    if deposit:
                        self.log_msg("deposit_runes clr.ORANGE Found")
                        self.mouse.move_to(deposit.random_point())
                        red_click = self.mouse.click(check_red_click=True)

                        if red_click:
                            self.log_msg("Clicked deposit")
                            return True  # Successfully clicked deposit

                        else:
                            self.log_msg("Can't find rune deposit location")
                            if self.is_player_idle3():
                                color_retries += 1
                                time.sleep(0.5)                         
                                continue  # Retry finding the deposit color
                            else:
                                self.log_msg("cry")
                    else:
                        self.log_msg("Can't find deposit color")
                        color_retries += 1
                        time.sleep(0.5)
                        continue  # Retry finding the deposit color

                self.log_msg("Failed to find deposit color after maximum retries")
                return False

            else:
                self.log_msg("No runes found to deposit")
                return False
        else:
            return True

    def arerunesgone(self, max_color_retries=20, api_s=StatusSocket(), api_m=MorgHTTPSocket()):
        if self.pouchcheck():    
            self.log_msg("deposit_runes")
            runes = api_m.get_first_occurrence([554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565])
            
            if runes:
                self.log_msg("deposit_runes get_first_occurrence")
                color_retries = 0

                while runes and color_retries < max_color_retries:
                    time.sleep(0.5)
                    color_retries += 1
                    runes = api_m.get_first_occurrence([554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565])

                if not runes:
                    time.sleep(random.uniform(0.5, 0.75))
                    self.log_msg("Runes are gone")
                    return True
                else:
                    self.log_msg("Max retries reached but runes are still present")
                    return False
            else:
                self.log_msg("# No runes found initially")
                return False
        else:
                return True

    #all Fragment Logic

    def essencecinventorycheck(self, api_s = StatusSocket(), api_m = MorgHTTPSocket()):
        self.log_msg("minerockcheck")
        if self.minerockcheck():
            return True
        
        self.log_msg("minerockcheck False")
        return False

    def guardian_fragments(self): # Local fuctions Called: none
        api_s = StatusSocket()
        item_id = 26878

        for _ in range(50):  # Retry 50 times for the item amount condition
            item_amount = api_s.get_inv_item_stack_amount(item_id)
        
            if item_amount > 140:
                self.log_msg(f"Log {item_amount} fragments")
                self.log_msg("Looking for climb")

                for _ in range(5):  # Retry 5 times for finding the climb
                    mineclimb = self.get_nearest_tag(clr.YELLOW)
                    if mineclimb:
                        self.mouse.move_to(mineclimb.random_point())
                        red_click = self.mouse.click(check_red_click=True)
                        if red_click:
                            self.log_msg("Leaving the mine")
                            if self.is_player_idle3():
                                return True
                            else:
                                self.log_msg("guardian_fragments idle error")
                                return False
                            
                        else:
                            self.log_msg("Can't find red click")
                            return False
                    time.sleep(0.5)  # Add a delay between retries

                self.log_msg("Can't find climb after 5 retries.")
                return False
            else:
                time.sleep(2)  # Add a delay between retries for the item amount condition

        self.log_msg("Can't meet item amount condition after 20 retries.")
        return False

    def minerockcheck(self, api_s=StatusSocket(), api_m=MorgHTTPSocket()):
        self.log_msg(f"Fragment check")
        item_id = 26878
        item_amount = api_s.get_inv_item_stack_amount(item_id)
        self.log_msg(f"Logged {item_amount} fragments")
        
        if item_amount < 50:
            if self.minerock():
                return True
            else:
                self.log_msg("Failed to mine fragments")
                return False
        else:
            return True

    def minerock(self, api_s=StatusSocket(), api_m=MorgHTTPSocket()):
        item_id = 26878
        if self.redclickcheck():
            time.sleep(1)
            self.log_msg("Successfully performed red click")
            for _ in range(40):  # Retry 40 times for the item amount condition
                self.gamecheckfinish()
                item_amount = api_s.get_inv_item_stack_amount(item_id)
                self.log_msg("Mining and portal loop")
                self.log_msg(f"Current fragment count: {item_amount}")
                time.sleep(1)
                
                if item_amount > 60:
                    self.log_msg(f"Logged {item_amount} fragments")
                    return True  # Successfully logged fragments

                if self.portallogic():
                    self.log_msg("Portal check error, exiting mining loop")
                    return False

            self.log_msg("Failed to log fragments after 40 retries")
            return False

        else:
            self.log_msg("minerock Failed at redclickcheck")
            return False

    def interact_with_bench(self): # Local fuctions Called: none
        self.log_msg("looking for bench")
        bench = self.get_nearest_tag(clr.RED)
        if bench:
            self.log_msg("bench found")
            self.mouse.move_to(bench.random_point())
            red_click = self.mouse.click(check_red_click=True)
            return True
        else:
            self.log_msg("Bench not found")
            return False

    def wait_for_crafting_xp(self, api_m = MorgHTTPSocket()): # Local fuctions Called: none
        self.log_msg("Looking for exp")
        if api_m.wait_til_gained_xp(skill="Crafting", timeout=10):
            self.log_msg("detected exp")
            return True
        else:
            self.log_msg("not found exp")
            return False

    #all bench Logic

    def bench(self): # Local fuctions Called: minerockcheck, inventorycheck, interact_with_bench, wait_for_crafting_xp, is_player_idle
        if  self.essencecinventorycheck():
            if self.fragcheck():               
                self.log_msg("interact_with_bench")
                if self.interact_with_bench():
                    self.log_msg("wait_for_crafting_xp")
                    if self.wait_for_crafting_xp():
                        self.log_msg("is_player_idle")
                        if self.essencecheck():
                            self.log_msg("is_player_idle True")
                            return True
                            
                        else:
                            self.log_msg("is_player_idle False")
                            return False
                    else:
                        self.log_msg("issue with wait for crafting XP gain")
                        return False
                else:
                    self.log_msg("interact_with_bench issue")
                    return False
            else:
                self.log_msg("Frags detected skipping bench")
                return True
        else:
            self.log_msg("essencecinventorycheck False")
            return False
            
    def bench2(self): # Local fuctions Called: interact_with_bench, wait_for_crafting_xp, is_player_idle2
        self.log_msg("benchnoportal")
        if self.fragcheck():
                self.log_msg("benchnoportal interact_with_bench")
                if self.interact_with_bench():
                    self.log_msg("benchnoportal wait_for_crafting_xp")
                    if self.wait_for_crafting_xp():
                        if self.essencecheck():
                            return True
                        
                        else:
                            self.log_msg("Player not idle after crafting2")
                            return False
                    else:
                        self.log_msg("Failed to wait for crafting XP gain2")
                        return False
                else:
                    self.log_msg("Can't perform red click2")
                    return False
        else:
            self.log_msg("Frags detected skipping bench")
            return True


    #rune location Logic

    def guardian_stones(self, probability_catalytic=0.5):
        # Calculate weights based on the probability_catalytic option
        weight_catalytic = probability_catalytic
        weight_elemental = 1 - probability_catalytic

        choices = ['catalytic_runecraft', 'elemental_runecraft']
        weights = [weight_catalytic, weight_elemental]

        chosen_option = random.choices(choices, weights=weights)[0]

        self.log_msg(f"Guardian {chosen_option}")

        if chosen_option == 'catalytic_runecraft':
            self.log_msg("Guardian catalytic_runecraft")
            if self.catalytic_runecraft():
                self.log_msg("Guardian catalytic_runecraft True")
                return True
            else:
               self.log_msg("Guardian catalytic_runecraft False")
               return False
        
            
        else:
            self.log_msg("Guardian elemental_runecraft")
            if self.elemental_runecraft():
                self.log_msg("Guardian elemental_runecraft True")
                return True
            else:
                self.log_msg("Guardian elemental_runecraft False")
                return False

    def fragcheck(self, api_s = StatusSocket(), api_m = MorgHTTPSocket()):
        if self.pouchcheck():
            return True
        else:
            return False
          
    def elemental_runecraft(self, api_s=StatusSocket(), api_m=MorgHTTPSocket()):
        while True:
            self.log_msg("Elemental Runecraft Start")
            region = self.win.gotrmouseover

            rune_images = {
                "air": imsearch.BOT_IMAGES.joinpath("gotr/air_rune.png"),
                "fire": imsearch.BOT_IMAGES.joinpath("gotr/fire_rune.png"),
                "earth": imsearch.BOT_IMAGES.joinpath("gotr/earth_rune.png"),
                "water": imsearch.BOT_IMAGES.joinpath("gotr/water_rune.png"),
            }

            rune_colors = {
                "air": clr.air,
                "fire": clr.fire,
                "earth": clr.earth,
                "water": clr.water,
            }

            for rune_name, rune_img in rune_images.items():
                rune_locations = imsearch.search_img_in_rect(rune_img, region, confidence=0.4)

                if rune_locations:
                    self.log_msg(f"Found rune: {rune_name}")  # Log the found rune
                    color_tag = self.get_nearest_tag(rune_colors[rune_name])

                    if color_tag:
                        self.log_msg(f"Rune color: {rune_name}")  # Log the color of the found rune
                        self.mouse.move_to(color_tag.random_point())
                        red_click = self.mouse.click(check_red_click=True)
                        self.log_msg("runecraft:redclick and move")
                        if red_click:
                            self.log_msg("Runecraft idlecheck")
                            if self.is_player_idle3():
                                self.log_msg("Runecraft am idle")
                                altar = self.get_nearest_tag(clr.PINK)
                                if altar:
                                    self.log_msg("found pink")
                                    return True
                            else:
                                self.log_msg("runecraft: idle issue")
                                altar = self.get_nearest_tag(clr.PINK)
                                if altar:
                                    self.log_msg("found pink")
                                    return True
                        else:
                            self.log_msg("runecraft:redlick issue")
                            altar = self.get_nearest_tag(clr.PINK)
                            if altar:
                                self.log_msg("found pink")
                                return True
                    else:
                        self.log_msg("runecraft:color issue")
                        altar = self.get_nearest_tag(clr.PINK)
                        if altar:
                            self.log_msg("found pink")
                            return True               

    def catalytic_runecraft(self, api_s=StatusSocket(), api_m=MorgHTTPSocket()):
        while True:
            self.log_msg("catalytic_runecraft_Start")
            region = self.win.gotrmouseover

            rune_images = {
                "cosmic": imsearch.BOT_IMAGES.joinpath("gotr/cosmic_rune.png"),
                "nature": imsearch.BOT_IMAGES.joinpath("gotr/nature_rune.png"),
                "death": imsearch.BOT_IMAGES.joinpath("gotr/death_rune.png"),
                "blood": imsearch.BOT_IMAGES.joinpath("gotr/blood_rune.png"),
                "law": imsearch.BOT_IMAGES.joinpath("gotr/law_rune.png"),
                "mind": imsearch.BOT_IMAGES.joinpath("gotr/mind_rune.png"),
                "chaos": imsearch.BOT_IMAGES.joinpath("gotr/chaos_rune.png"),
                "body": imsearch.BOT_IMAGES.joinpath("gotr/body_rune.png"),
            }

            rune_colors = {
                "law": clr.law,
                "body": clr.body,
                "chaos": clr.chaos,
                "blood": clr.blood,
                "cosmic": clr.cosmic,
                "nature": clr.nature,
                "death": clr.death,
                "mind": clr.mind,
            }

            for rune_name, rune_img in rune_images.items():
                rune_locations = imsearch.search_img_in_rect(rune_img, region, confidence=0.4)

                if rune_locations:
                    self.log_msg(f"Found rune: {rune_name}")  # Log the found rune
                    color_tag = self.get_nearest_tag(rune_colors[rune_name])

                    if color_tag:
                        self.log_msg(f"Rune color: {rune_name}")  # Log the color of the found rune
                        self.mouse.move_to(color_tag.random_point())
                        red_click = self.mouse.click(check_red_click=True)
                        self.log_msg("runecraft:redclick and move")
                        if red_click:
                            self.log_msg("Runecraft idlecheck")
                            if self.is_player_idle3():
                                self.log_msg("Runecraft am idle")
                                altar = self.get_nearest_tag(clr.PINK)
                                if altar:
                                    self.log_msg("found pink")
                                    return True
                            else:
                                self.log_msg("runecraft: idle issue")
                                altar = self.get_nearest_tag(clr.PINK)
                                if altar:
                                    self.log_msg("found pink")
                                    return True
                        else:
                            self.log_msg("runecraft:redlick issue")
                            altar = self.get_nearest_tag(clr.PINK)
                            if altar:
                                self.log_msg("found pink")
                                return True
                    else:
                        self.log_msg("runecraft:color issue")
                        altar = self.get_nearest_tag(clr.PINK)
                        if altar:
                            self.log_msg("found pink")
                            return True

                

#New Portal spawn Logic

    def portallogic(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        if self.portalgreen():
            self.log_msg("portallogic: portalgreen True")
            if self.portaldespawn():
                self.log_msg("portallogic: portaldespawn True")
                if self.portalpart1():
                    self.log_msg("portallogic: portalpart1 True")
                    if self.pouchs():
                        self.log_msg("portallogic: pouch True")
                        if self.portalpart2():
                            self.log_msg("portallogic: portalpart2 True")
                            if self.pouchs2():
                                self.log_msg("portallogic: pouch2 True")
                                if self.portalpart3():
                                    time.sleep(random.uniform(0.5, 0.75))
                                    return True
                                
                                else:
                                    self.log_msg("portallogic: issue in portalpart3")
                                    return False
                            else:
                                self.log_msg("portallogic: issue in pouchs2")
                                return False
                        else:
                            self.log_msg("portallogic: issue in portalpart2")
                            return False
                    else:
                        self.log_msg("portallogic: issue in pouchs")
                        return False
                        
                else:
                    self.log_msg("portallogic: issue in portalpart1")
                    return False
            else:
                self.log_msg("portallogic: issue in portaldespawn")
                return False
        else:
            self.log_msg("portallogic: No Portal found")
            return False

    def portalpart1(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        self.log_msg("Portal:looking for cyan")
        rocky = self.get_nearest_tag(clr.CYAN)
        if rocky:
            self.log_msg("Portal:cyan found")
            self.mouse.move_to(rocky.random_point())   
            red_click = self.mouse.click(check_red_click=True)
            self.log_msg("Portal:cyan redclick and move")
            if red_click:
                self.log_msg("Portal:redclick and move passed")
                if self.essencechecknoportal():
                    self.log_msg("Portal:am idle")
                    self.gamecheckfinishportal()
                    self.log_msg("Portal:into pouches")
                    return True
                    
                else:
                    self.log_msg("Portal:idle issue")
                    return False      
            else: 
                self.log_msg("Portal:cyan redclick and move")       
                return False
        else:
            self.log_msg("Portal:looking for cyan")
            return False

    def portalpart2(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        self.log_msg("Portal:pouchcheck")
        if self.pouchcheck():
            rocky2 = self.get_nearest_tag(clr.CYAN)
            self.log_msg("Portal:looking for Cyan again")
            if rocky2:
                self.log_msg("Portal:found cyan")
                self.mouse.move_to(rocky2.random_point())
                red_click = self.mouse.click(check_red_click=True)
                self.log_msg("Portal:cyan redclick and move again")
                if red_click:
                    self.log_msg("Portal:cyan redclick is good")
                    self.log_msg("Portal:idle check again")
                    if self.essencechecknoportal():   
                        return True

                    else: 
                        self.log_msg("Portal:issues idle check again")       
                        return False
                else:
                    self.log_msg("Portal:issues at cyan redclick and move again")
                    return False
            else:
                self.log_msg("Portal:issue at Cyan again")
                return False
        else:
            self.log_msg("Portal: pouch full")
            if self.portalleave():
                return True    
            else:
                self.log_msg("Portal:issues portalleave")       
                return False

    def portalpart3(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        self.log_msg("Portal:pouchcheck")
        if self.pouchcheck():
            rocky2 = self.get_nearest_tag(clr.CYAN)
            self.log_msg("Portal:looking for Cyan again")
            if rocky2:
                self.log_msg("Portal:found cyan")
                self.mouse.move_to(rocky2.random_point())
                red_click = self.mouse.click(check_red_click=True)
                self.log_msg("Portal:cyan redclick and move again")
                if red_click:
                    self.log_msg("Portal:cyan redclick is good")
                    self.log_msg("Portal:idle check again")
                    if self.essencechecknoportal():   
                        self.log_msg("Portal: pouch full")
                        if self.portalleave():
                            return True    
                        else:
                            self.log_msg("Portal:issues portalleave")       
                            return False
                    else: 
                        self.log_msg("Portal:issues idle check again")       
                        return False
                else:
                    self.log_msg("Portal:issues at cyan redclick and move again")
                    return False
            else:
                self.log_msg("Portal:issue at Cyan again")
                return False
        else:
            self.log_msg("Portal: pouch full")
            if self.portalleave():
                return True    
            else:
                self.log_msg("Portal:issues portalleave")       
                return False

    def portalgreen(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        self.log_msg("Looking for Portal")
        portal = self.get_nearest_tag(clr.GREEN)
        if portal:
            if self.pouchcheck():
                self.log_msg("Portal found Green")
                time.sleep(0.5)
                self.mouse.move_to(portal.random_point())
                red_click = self.mouse.click(check_red_click=True)
                if red_click:
                    self.log_msg("red click Portal found")
                    return True
                else:
                    self.log_msg("red click  failed on Portal")
                    if  self.is_player_idle3():
                        self.portalgreen()
                        return True
                    else:
                        return False      
            else:

                self.log_msg("Guardianessence check")
                if self.Guardianessence():
                    self.log_msg("Portal found Green2")
                    time.sleep(0.5)
                    self.mouse.move_to(portal.random_point())
                    red_click = self.mouse.click(check_red_click=True)
                    if red_click:
                        self.log_msg("G red click Portal found")
                        return True
                    else:
                        self.log_msg("G red click  failed on Portal")
                        return False              
                else: self.log_msg("You have more than 10 Essence.")
                return False
        else:
            self.log_msg("No Portal found")
            return False   

    def Guardianessence(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()): # Local fuctions Called: none
        inventory_data = api_m.get_inv2()
        GUARDIAN_ESSENCE = inventory_data.get(26879, 0)
        if GUARDIAN_ESSENCE > 10:
            self.log_msg("You have more than 10 Essence.")
            return False
        else:
            self.log_msg("You have 10 or fewer Essence.")
            return True

    def portalleave(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        leave = self.get_nearest_tag(clr.GREEN)
        if leave:
            self.log_msg("Portal:found green we leaving cya")
            self.mouse.move_to(leave.random_point())
            red_click = self.mouse.click(check_red_click=True)
            if red_click:
                self.log_msg("Portal:found last reclick")
                if self.is_player_idle3:
                    time.sleep(random.uniform(1.5, 2))
                    return True
                else:
                    self.log_msg("Portal:issue at last idle")
                    return False
                    
            else:
                self.log_msg("Portal:issue at last redclick")
                return False
        else:
            self.log_msg("Portal:issue at trying to leave")
            return False

    def portaldespawn(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        while True:
            check_portal = self.get_nearest_tag(clr.GREEN)
            self.log_msg("portaldespawn GREEN found")

            if check_portal:
                self.log_msg("portaldespawn loop")
                if self.is_player_idle3():
                    if self.get_nearest_tag(clr.GREEN):
                        self.log_msg("despawncheck loop am idle")
                        return True
                    else:
                        self.log_msg("portaldespawn am idle and can't see portal")
                        self.log_msg("Might need bench recheck here")
                        return False      

                else:
                    self.log_msg("portaldespawn loop sleep")
                    time.sleep(0.25)
                    continue
            else:
                self.log_msg("portaldespawn is not present")
                if self.is_player_idle3():
                    check_portal2 = self.get_nearest_tag(clr.GREEN)
                    if check_portal2:
                        self.log_msg("portaldespawn GREEN found")
                        return True
                    else:

                        return False
   
    #Pouch Logic + talismans

    def essencecheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20): 
        for _ in range(max_retries):
            inventory_data = api_m.get_inv2()
            GUARDIAN_ESSENCE = inventory_data.get(26879, 0)
            
            if GUARDIAN_ESSENCE > 19:  # You have more than 20 Essence
                self.log_msg("You have more than 19 Essence.")
                return True
            else:
                self.gamecheckfinishportal()
                portal = self.portallogic()
                self.log_msg("Less than 19 Essence")
                if portal:
                    return False
                time.sleep(1)

        self.log_msg("essencecheck error")
        self.gamecheckfinishportal()
        return False

    def essencechecknoportal(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20): 
        for _ in range(max_retries):
            inventory_data = api_m.get_inv2()
            GUARDIAN_ESSENCE = inventory_data.get(26879, 0)
            
            if GUARDIAN_ESSENCE > 19:  # You have more than 20 Essence
                self.log_msg("pYou have more than 19 Essence.")
                return True
            else:
                self.gamecheckfinishportal()
                self.log_msg("pLess than 19 Essence")
                time.sleep(1)

        self.log_msg("pessencecheck error")
        self.gamecheckfinishportal()
        return False
    #def pouchlogic(self, api_m=MorgHTTPSocket(),api_s = StatusSocket()):
            
    def repairpouch(self, api_m=MorgHTTPSocket()): # Local fuctions Called: none
        pyautogui.hotkey("f9")
        time.sleep(random.uniform(1.3, 1.75))
        self.log_msg("Looking for contact npc")
        repair = imsearch.BOT_IMAGES.joinpath("gotr/repair_pouch.png")
        repair = imsearch.search_img_in_rect(repair, self.win.control_panel)
        self.log_msg("contact npc found")
        moverepair = self.mouse.move_to(repair.random_point())
        self.mouse.click()

        for _ in range(20):
            idle = api_m.get_is_player_idle()
            if idle:
                self.log_msg("contact darkmage")
                time.sleep(random.uniform(1, 1.75))
                pyautogui.press('space')
                time.sleep(random.uniform(1, 1.75))
                pyautogui.press('2')
                time.sleep(random.uniform(1, 1.75))
                pyautogui.press('space')
                time.sleep(random.uniform(0.3, 0.75))
                pyautogui.hotkey("F10")
                # pyautogui.press('space')
                return True
            else:
                time.sleep(1)
                self.log_msg("waiting for animation")

        self.log_msg("contact darkmage failed")

    def pouchs(self, api_m=MorgHTTPSocket(),api_s = StatusSocket()): # Local fuctions Called: none
        if ocr.find_text("0", self.win.control_panel, ocr.PLAIN_11, [clr.CYAN, clr.OFF_CYAN]):
            self.log_msg("pouchcheck found 0")
            pouch_ids = [5512, 5514, 26784]
            pouchs = api_s.get_inv_item_indices(pouch_ids)
            if pouchs:
                self.Moverandomclick(pouchs)
                self.log_msg("found pouch")
                return True
            else:
                return False
        else:
            # Handle the case when pouchtext is not "0"
            self.log_msg("pouchcheck not 0")
            return True

    def pouchs2(self, api_m=MorgHTTPSocket(),api_s = StatusSocket()): # Local fuctions Called: none
        if ocr.find_text("0", self.win.control_panel, ocr.PLAIN_11, [clr.CYAN, clr.OFF_CYAN]):
            self.log_msg("pouchcheck2 found 0")
            pouch_ids = [5509, 5510, 26784]
            pouchs = api_s.get_inv_item_indices(pouch_ids)
            if pouchs:
                self.Moverandomclick(pouchs)
                self.log_msg("found pouch2")
                return True
            else:
                return False
        else:
            # Handle the case when pouchtext is not "0"
            self.log_msg("pouchcheck2 not 0")
            return True

    def pouchsaltar(self, api_m=MorgHTTPSocket(),api_s = StatusSocket()):
            self.log_msg("pouchcheck found 0")
            pouch_ids = [5512, 5514, 26784]
            pouchs = api_s.get_inv_item_indices(pouch_ids)
            if pouchs:
                self.Moverandomclick(pouchs)
                self.log_msg("found pouch")
                return True
            else:
                return False
    
    def pouchsaltar2(self, api_m=MorgHTTPSocket(),api_s = StatusSocket()):
            self.log_msg("pouchcheck found 0")
            pouch_ids = [5509, 5510, 5512, 26784]
            pouchs = api_s.get_inv_item_indices(pouch_ids)
            if pouchs:
                self.Moverandomclick(pouchs)
                self.log_msg("found pouch")
                return True
            else:
                return False

    def droptalismans(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()): # Local fuctions Called: none
        talismans = api_s.get_inv_item_indices([26887, 26888, 26889, 26890, 26891, 26892, 26893, 26894, 26895, 26896, 26897, 26898])
        self.drop(talismans)
        return

    #Idle/retry Logic

    def is_player_idle(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20): # Local fuctions Called: portal_check
            for _ in range(max_retries):
                self.log_msg("is_player_idle loop")
                time.sleep(1)
                portal = self.portallogic()
                if portal:
                    self.log_msg("is_player_idle portal")
                    return False
                
                else:
                    if api_m.get_is_player_idle():
                        self.log_msg("is_player_idle True")
                        return True
                
            return False

    def is_player_idle2(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20): # Local fuctions Called: portal_check
            for _ in range(max_retries):
                time.sleep(1)
                portal = self.portallogic()
                self.log_msg("is_player_idle2")
                if portal:
                    return False
                

                else:
                    if api_m.get_is_player_idle():
                        self.log_msg("is_player_idle2 True")
                        return True
                
            return False

    def is_player_idle3(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20): # Local fuctions Called: none
            for _ in range(max_retries):
                time.sleep(1)
                self.log_msg("is_player_idle3 ")
                if api_m.get_is_player_idle():
                    self.log_msg("is_player_idle3 True")
                    return True

            return False

    def pinkcheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=2): # Local fuctions Called: none
        for _ in range(max_retries):
            time.sleep(1)
            self.log_msg("pinkcheck ")
            if self.get_nearest_tag(clr.PINK):
                self.log_msg("pinkcheck Found PINK")
                return True
            else:
                self.log_msg("pinkcheck PINK not found retrying")
                #if self.guardian_stones():
                

        return False

    def redclickcheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket(), max_retries=20):
        for _ in range(max_retries):
            time.sleep(1)
            rock = self.get_nearest_tag(clr.PURPLE)
            self.log_msg("redclickcheck ")

            if rock:
                self.log_msg(f"Found purple rock at {rock.random_point()}")               
                self.mouse.move_to(rock.random_point())
                self.log_msg("Successfully moved mouse to the rock")
                red_click = self.mouse.click(check_red_click=True)
                    
                if red_click:
                    self.log_msg("redclickcheck Found")
                    return True
                    
                else:
                    self.log_msg("redclickcheck fail retrying")
                
            else:
                self.log_msg("redclickcheck can't find rock colour")


        return False
          
    #Exception function Logic

    def elemental_runecraftcheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
            api_m = MorgHTTPSocket()
            api_s = StatusSocket()
            self.log_msg("Elemental game check")
            region = self.win.gotrmouseover

            rune_images = {
                "air": imsearch.BOT_IMAGES.joinpath("gotr/air_rune.png"),
                "fire": imsearch.BOT_IMAGES.joinpath("gotr/fire_rune.png"),
                "earth": imsearch.BOT_IMAGES.joinpath("gotr/earth_rune.png"),
                "water": imsearch.BOT_IMAGES.joinpath("gotr/water_rune.png"),
            }

            rune_colors = {
                "air": clr.air,
                "fire": clr.fire,
                "earth": clr.earth,
                "water": clr.water,
            }

            rune_locations = {}

            for rune_name, rune_img in rune_images.items():
                rune_locations[rune_name] = imsearch.search_img_in_rect(rune_img, region, confidence=0.4)

                if rune_locations[rune_name]:
                    color_tag = self.get_nearest_tag(rune_colors[rune_name])
                    if color_tag:
                        self.log_msg("Elemental game check still going")
                        return False
                    else:
                        self.log_msg("Elemental game check game ended")
                        return True
                else:
                        self.log_msg("Elemental game check game ended")
                        return True   
                        
    def gamecheckfinish(self,api_m=MorgHTTPSocket()): # Local fuctions Called: repairpouch, handle_starting_spot
        if self.chatbox_textred("The Great"):
            self.log_msg("Game end detected checking for start")
            if self.chatbox_textred("active!"):
                self.log_msg("new game just started")
                return

            else:
                self.log_msg("Guardian Died")
                self.postgame()
                raise CustomErrorClass()
        
        if self.chatbox_textGuardian("The Great"):
            self.log_msg("game finished")
            self.postgame()
            raise CustomErrorClass()
        else:
            self.log_msg("game is still going")
    
    def gamecheckfinishportal(self,api_m=MorgHTTPSocket()): # Local fuctions Called: repairpouch, handle_starting_spot
        if self.chatbox_textred("The Great"):
            if self.elemental_runecraftcheck():
                self.log_msg("Guardian Died")
                self.postgameportal()
                raise CustomErrorClassportal()
        
        if self.chatbox_textGuardian("The Great"):
            self.log_msg("game finished")
            self.postgameportal()
            raise CustomErrorClassportal()
        else:
            self.log_msg("game is still going")
    
    def postgame(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()): # Local fuctions Called: repairpouch, handle_starting_spot
        self.log_msg("gamefinshed setting up for new game")
        if self.repairpouch():
            if self.handle_starting_spot(api_m):

                return
            else:
                self.log_msg("crical error at handle_starting_spot")
                exit()
        else:    
            self.log_msg("crical error at repairpouch(check runes)")
            exit()

    def postgameportal(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        self.log_msg("gamefinshed setting up for new game")
        leave_portal = self.get_nearest_tag(clr.GREEN)
        if leave_portal:
            self.mouse.move_to(leave_portal.random_point())
            self.mouse.click()
            time.sleep(2.5)
            if self.repairpouch():
                    if self.handle_starting_spot(api_m):

                        return
                    else:
                        self.log_msg("crical error at handle_starting_spot")
                        exit()
            else:    
                    self.log_msg("crical error at repairpouch(check runes)")
                    exit()

    #essence Logic

    def inventorycheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()): # Local fuctions Called: none


        inventory_data = api_m.get_inv2()
        ESSENCE = inventory_data.get(26879, 0)
        self.log_msg(f"Actual Essence quantity: {ESSENCE}")

        if ESSENCE > 15:
            self.log_msg("You have more than 15 Essence.")
            return True
        else:
            self.log_msg("You have 15 or fewer Essence.")
            return False


    # Unused functions
    def fillpouch(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()): #unused
        self.pouchs()
        bench = self.get_nearest_tag(clr.RED)
        if bench:
            self.mouse.move_to(bench.random_point())
            red_click = self.mouse.click(check_red_click=True)
            if red_click:
                exp = api_m.wait_til_gained_xp(skill="Crafting", timeout=10)
                if exp:
                    idle = self.is_player_idle()
                    if idle: 
                        return True
                    else:
                        time.sleep(1)
                        self.log_msg("waiting")
                                   
                else:
                    return False        

            else:
                return False
        else:
            return False

    def pouchcheck(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        if ocr.find_text("0", self.win.control_panel, ocr.PLAIN_11, [clr.CYAN, clr.OFF_CYAN]):
            self.log_msg("pouchcheck found 0")
            return True
        else:
            # Handle the case when pouchtext is not "0"
            self.log_msg("pouchcheck not 0")
            return False

    def pouchcheck2(self, api_m=MorgHTTPSocket(), api_s=StatusSocket()):
        if ocr.find_text("0", self.win.control_panel, ocr.PLAIN_11, [clr.CYAN, clr.OFF_CYAN]):
            self.log_msg("pouchcheck found 0")
            return True
        else:
            # Handle the case when pouchtext is not "0"
            self.log_msg("pouchcheck not 0")
            return False

    def get_pouches(self,api_m=MorgHTTPSocket()) -> List[dict]: #unused
        inv = api_m.get_inv()
        pouches = [item for item in inv if item["id"] in [5509, 5510, 5512, 5514, 26784]]
        return pouches

    def click_inventory_item(self, item_location): #unused
        self.mouse.move_to(self.win.inventory_slots[item_location].random_point(),mouseSpeed="fastest")
        self.mouse.click()
     
    def inventoryfullcheck(self, max_retires=30, retry_delay=1): #unused
        api_s = StatusSocket()
        for _ in range(max_retires):

            if api_s.get_is_inv_full():
                return True  
            time.sleep(retry_delay)
        return False          


     
class CustomErrorClassportal(Exception):
    def __init__(self, message=None):
        if message is None:
            message = (
                "Game end in portal cring"
                )
        super().__init__(message)


class CustomErrorClass(Exception):
    def __init__(self, message=None):
        if message is None:
            message = (
                "Gameend"
            )
        super().__init__(message)

























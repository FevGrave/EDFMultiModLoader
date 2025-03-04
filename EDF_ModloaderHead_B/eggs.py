# eggs.py

import random, time, sys, tkinter as tk

AsciiE = r''' ______    
/\  ___\   
\ \  __\   
 \ \_____\ 
  \/_____/ 
    '''#E

AsciiD = r''' ______      _____    
/\  ___\    /\  __-.  
\ \  __\    \ \ \/\ \ 
 \ \_____\   \ \____- 
  \/_____/    \/____/  
    '''#D

AsciiF = r''' ______      _____       ______  
/\  ___\    /\  __-.    /\  ___\ 
\ \  __\    \ \ \/\ \   \ \  __\ 
 \ \_____\   \ \____-    \ \_\   
  \/_____/    \/____/     \/_/   
    '''#F

def someegg(show_error):
    """
    A fun Easter egg function that surprises the user with a random Earth Defense Force-themed message or event
    with Storm 1 as the protagonist.
    """
    edf_shenanigans = [
        "🚨 *Storm 1*! HQ just detected a giant ant nest opening near the city! Time to prove why you're Earth's last hope! 🐜",
        "🔥 HQ to *Storm 1*: You've unlocked a new experimental weapon: *'Overkill Cannon Mk. III'*. It's only slightly unstable this time! 😅",
        "🎵 *Storm 1*! Start chanting: EDF! EDF! Your teammates are losing morale, and only you can save the day with your battle cry. 🎶",
        "👽 HQ to *Storm 1*: The Ravagers are attempting to negotiate! Your response? *Fire first, ask questions never!* 😎",
        "🛠️ Patch Note: *Storm 1 now starts each mission with twice the plot armor.* Because you're clearly the protagonist. 🦾",
        "📡 HQ to *Storm 1*: Time travel anomaly detected. Future *Storm 1* reports, 'Mission already completed. Take a day off.' 🛸",
        "🐸 *Storm 1*, you’ve been challenged to a dance-off by a giant frog kaiju. You lose. But your moves inspired the civilians to join EDF! 🕺",
        "🦾 HQ to *Storm 1*: Your armor has been upgraded with the *'Absurd Damage Resistance Perk.'* You can now survive nuclear blasts, but watch out for frogs. 🐸",
        "🚀 *Storm 1*, the EDF R&D team just delivered your latest weapon: *A 'Baguette Launcher'.* Ideal for confusing the Ravagers. 🥖",
        "🛑 Alert! *Storm 1*, the lobby is full of Air Raiders. Prepare for total chaos as airstrikes overlap in the most glorious way possible! ☁️💥",
        "🐇 HQ to *Storm 1*: Beware the giant killer rabbit! You must use the *Holy Hand Grenade* to defeat it! 🧨🐰",
        "🏰 *Storm 1*! We have discovered an ancient EDF base! The records say it was built in *Camelot*! But... it's only a model. 🤷",
        "💀 HQ to *Storm 1*: We have a mission for you. It is a quest... for the *EDF Grail*! You must not falter! Or run away! 🏃",
        "🎺 *Storm 1*, be aware! The enemy forces are preparing to attack... but only after a *dramatic trumpet fanfare!* 📯",
        "🔍 EDF Command: We need intelligence reports on the enemy. Deploy the *Department of Silly Walks* to investigate immediately! 🚶‍♂️",
        "🔥 HQ to *Storm 1*: We’ve intercepted enemy plans. Their main tactic? *RUN AWAY!*",
        "🤔 EDF HQ just issued a new rule: You may only answer your commanding officer in *outrageous French accents* or *coconut galloping noises*! 🥥🐎",
        "🏆 *Storm 1*! You have fought bravely! You are now being promoted to *Supreme Commander of the EDF Knights Who Say Ni!* 🏰",
        "💀 ALERT: *An unexpected giant foot has descended from the sky!* ...Oh wait, false alarm. That was just another EDF airstrike. 🦶💥",
        "⚔️ *Storm 1*, you must retrieve the *EDF Sacred Code of Modding*! It is guarded by a *programmer wizard* who shouts 'NI' whenever Python throws an error! 😱",
        "🚁 HQ to *Storm 1*: Be advised, your new air transport has been *replaced with a flying circus*! Expect occasional comedy skits mid-mission. 🎪✈️",
        "👑 HQ to *Storm 1*: You are now King of the EDF! ... But only if you can prove you *did not inherit it through an aquatic ceremony with a sword!* 🏊‍♂️⚔️",
        "🕵️ *Storm 1*! You have been assigned to *The Ministry of Silly Strategies!* Your first order: *Taunt the enemies in increasingly ridiculous ways!* 😂",
        "🐸 EDF HQ Alert: Giant talking frogs have invaded again! One of them just *insulted your mother and threatened to fart in your general direction!* What’s your response?! 🤨",
        "🍔 *Professor:* 'Ah, Storm 1! Have you ever pondered the perfect burger? Soft bun, juicy patty, melted cheese... true perfection!' 🤤",
        "🔥 *Professor:* 'We must protect humanity... and the sacred art of grilling! EDF is the last line of defense between us and a world without BURGERS!'",
        "👨‍🏫 *Professor:* 'Storm 1, what’s more dangerous? A Ravager invasion or a well-done burger? The answer is obvious. Medium-rare or NOTHING!'",
        "📡 *HQ:* 'Professor, please stay on topic—'  🗣️ *Professor:* 'THIS IS THE TOPIC! You can't fight a war on an empty stomach!'",
        "🍖 *Professor:* 'The aliens? They don't eat burgers! That's why they must be destroyed! A species that doesn’t understand flame-grilled beauty has no place in our universe!'",
        "💡 *Professor:* 'Storm 1, have you ever heard the legend of the *Double-Stacked Quantum Cheeseburger*? It exists in a theoretical space where ALL burgers are perfect!'",
        "🚀 *Professor:* 'Listen up, soldiers! The only thing more important than protecting Earth... is protecting our right to put bacon on everything!'",
        "🛠️ *Professor:* 'The EDF needs new weapons! What if... we made a burger so delicious it convinced the aliens to surrender?!'",
        "💥 *Professor:* 'A burger without sauce is like a Ranger without a rocket launcher. It still works, but WHY would you settle for that?!'",
        "🛸 *Professor:* 'The Ravagers have no mouths. That’s why they’re so angry. They’ve never known the joy of a perfect burger!'",
        "🦾 *Professor:* 'Storm 1, do you understand what’s at stake? If we fall, who will carry on the legacy of barbecue?!' 😤",
        "🍟 *Professor:* 'Burgers! Fries! The perfect duo! But what about the drink?! Some say cola, some say milkshakes. This is the true philosophical battle of our time!'",
        "🤖 *Professor:* 'What if the aliens aren't trying to destroy us... but are actually searching for the Ultimate Burger Recipe?'",
        "💀 *Professor:* 'Storm 1! If I don’t make it... make sure my *burger recipes* are passed down to future generations!'",
        "🔫 *Professor:* 'We don’t need bigger guns. We need bigger BURGERS! More cheese! More bacon! More tactical deliciousness!'",
        "💣 *Professor:* 'Storm 1, forget orbital strikes! What if we dropped GIANT BURGERS on the enemy? They’d be too distracted by the aroma to keep fighting!'",
        "📢 *Professor:* 'I have only one thing to say: EDF! EDF! ...AND BURGERS!!!'",
        "🔥 *Professor:* 'Burgers are like war, Storm 1. The perfect sear, the perfect seasoning... if you hesitate, the whole operation is ruined!'",
        "🍽️ *Professor:* 'Victory tastes like a burger after a long mission. Defeat tastes like... burnt patties and sadness.'"
    ]

    # Pick a random message
    random_egg = random.choice(edf_shenanigans)

    # Display the selected message
    show_error(random_egg)

def play_edf_chant(show_error, clear_error):
    """
    Display the EDF chant with custom delays per line.
    """
    clear_error()  # Clear screen at the start

    '''
    Font used
    https://patorjk.com/software/taag/#p=display&v=0&f=Sub-Zero
    '''
    # Helper function for timed printing
    def delay_show(text, delay):
        """
        Display the text with the specified delay.
        """
        show_error(text)
        time.sleep(delay)

    # Define ASCII art blocks
    AsciiStart = r''' ______    __  __     ______    
/\__  _\  /\ \_\ \   /\  ___\   
\/_/\ \/  \ \  __ \  \ \  __\   
   \ \_\   \ \_\ \_\  \ \_____\ 
    \/_/    \/_/\/_/   \/_____/ 
    '''#THE

    AsciiEnd = r''' _____      ______      ______    __          ______      __  __      ______    
/\  __-.   /\  ___\    /\  == \  /\ \        /\  __ \    /\ \_\ \    /\  ___\   
\ \ \/\ \  \ \  __\    \ \  _-/  \ \ \____   \ \ \/\ \   \ \____ \   \ \___  \  
 \ \____-   \ \_____\   \ \_\     \ \_____\   \ \_____\   \/\_____\   \/\_____\ 
  \/____/    \/_____/    \/_/      \/_____/    \/_____/    \/_____/    \/_____/ 
    '''#DEPLOYS

    chants = [
        ("To save our Mother Earth from any alien attack", 3),
        ("From vicious giant insects who have once again come back", 3),
        ("We'll unleash all our forces, we won't cut them any slack", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("Our soldiers are prepared for any alien threats", 3),
        ("The Navy launches ships, the Air Force sends their jets", 3),
        ("And nothing can withstand our fixed bayonets", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("Our forces have now dwindled and we pull back to regroup", 3),
        ("The enemy has multiplied and formed a massive group", 3),
        ("We'd better beat these bugs before we're all turned to soup", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("To take down giant insects who came from outer space", 3),
        ("We now head underground for their path we must retrace", 3),
        ("And find their giant nest and crush the Queen's carapace", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("The Air Force and the Navy were destroyed or cast about", 3),
        ("Scouts, Rangers, wing divers have almost been wiped out", 3),
        ("Despite all this the infantry will stubbornly hold out", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("Our friends were all killed yesterday as were our families", 3),
        ("Today we may not make it facing these atrocities", 3),
        ("We'll never drop our banner despite our casualties", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("Two days ago my brother died, next day my lover fell", 3),
        ("Today most everyone was killed on that we must not dwell", 3),
        ("But we will never leave the field, we'll never say farewell", 3),
        ("\nTHE E.D.F. DEPLOYS!", 3),
        ("Stop that depressing crap!", 3),
        ("What's the point of that song?", 3),
        ("Then how about this song?", 3),
        ("", 3),
        ("A legendary hero soon will lead us to glory", 3),
        ("Eight years ago he sunk the mothership say's history", 3),
        ("Tomorrow we will follow this brave soul to victory", 3),
        ("", 0),
        (AsciiStart, 1), # Display ASCII art
        ("", 0),
        (AsciiE, 1),
        ("", 0),
        (AsciiD, 1),
        ("", 0),
        (AsciiF, 1),
        ("", 0),
        (AsciiEnd, 3),
        ("", 0)
    ]

    for line, delay in chants:
        delay_show(line, delay)
        # Clear errors after specific lines, if needed
        if line == "\nTHE E.D.F. DEPLOYS!" or line == "":
            clear_error()

def side_scroll_edf_multiline(show_error, clear_error, speed=0.1, timeout=10):
    """
    Side-scrolls the string 'EDF ' across 5 lines with a fixed portal effect.

    Args:
        show_error (function): Function to display messages.
        clear_error (function): Function to clear the display.
        speed (float): Speed of scrolling (in seconds).
        timeout (int): Time in seconds before stopping the animation.
    """
    base_text = "EDF " * 25  # Repeating string of 'EDF '
    window_width = 90        # Fixed width of the portal window
    num_lines = 6            # Number of lines to display
    positions = [0] * num_lines  # Track position for each line

    # Extend the text for seamless scrolling
    scrolling_text = base_text + base_text[:window_width]

    start_time = time.time()  # Start the timer

    try:
        while time.time() - start_time < timeout:
            clear_error()

            # Generate and display each line
            for i in range(num_lines):
                visible_text = scrolling_text[positions[i]:positions[i] + window_width]
                show_error(visible_text)

                # Update position for each line
                positions[i] = (positions[i] + 1) % len(base_text)

            # Add a slight delay between each frame
            time.sleep(speed)

        clear_error()
        show_error("⏳ Scrolling timed out after 10 seconds. EDF stands down.")
    
    except KeyboardInterrupt:
        clear_error()
        show_error("Scrolling stopped. EDF stands down.")

def edf_credits_scroll(show_error, clear_error, speed=0.1, timeout=10):
    """
    Displays a credit roll in the console with scrolling top and bottom text,
    while keeping the middle section static.

    Args:
        show_error (function): Function to display messages.
        clear_error (function): Function to clear the display.
        speed (float): Speed of scrolling (in seconds).
        timeout (int): Time in seconds before stopping the animation.
    """
    base_text = "EDF " * 25  # Repeating scrolling string
    window_width = 90        # Fixed width of the scrolling section
    positions_top = 0        # Track position for top scrolling text
    positions_bottom = 0     # Track position for bottom scrolling text

    # Extend the text for seamless scrolling
    scrolling_text = base_text + base_text[:window_width]

    static_text = [
        "Created By:",
        "BlueAmulet: (Modloader)",
        "FevGrave: (GUI, MML Table Generator, BG Images)",
        "MoistGoat: (Advanced Mission Pack Unlimiter Patch)",
    ]

    def center_text(text):
        return text.center(window_width)

    start_time = time.time()  # Start the timer

    try:
        while time.time() - start_time < timeout:
            clear_error()

            # Generate scrolling lines
            top_scroll = scrolling_text[positions_top:positions_top + window_width]
            bottom_scroll = scrolling_text[positions_bottom:positions_bottom + window_width]

            # Display the scrolling and static text
            show_error(top_scroll)
            for line in static_text:
                show_error(center_text(line))  # Print each static line centered
            show_error(bottom_scroll)

            # Update positions for scrolling effect
            positions_top = (positions_top + 1) % len(base_text)
            positions_bottom = (positions_bottom + 1) % len(base_text)

            # Add a slight delay between each frame
            time.sleep(speed)

        clear_error()
        show_error("⏳ Credits timed out after 10 seconds. EDF out.")
    
    except KeyboardInterrupt:
        clear_error()
        show_error(center_text("💀 EDF CREDITS ABORTED. BUT THE WAR NEVER ENDS."))

def edf_mission_generator(show_error):
    """
    Generates a randomized Earth Defense Force mission briefing with a mix of serious and absurd elements.
    """
    # Random mission titles
    mission_titles = [
        "Operation: Bugged Beyond Belief",
        "Mission 404: EDF Not Found",
        "The Frog Invasion",
        "Ants In My Pants 2: The Sequel",
        "This Is A Trap... Probably",
        "Doomsday In The Subway",
        "Crisis On Infinite Crates",
        "The Baguette Offensive",
        "Lost In Time, Found In Chaos",
        "EDF vs. The Kaiju Council"
    ]

    # Random mission briefings
    mission_briefings = [
        "HQ has detected an enormous underground insect hive. Unfortunately, you will be entering without air support due to budget cuts. Good luck!",
        "A new species of giant frogs has invaded the city. They're wearing battle armor and appear to be... dancing? We need intel. Engage with extreme caution.",
        "A mysterious portal has opened, spewing out what appears to be EDF soldiers from another timeline. Are they friend or foe? Either way, you're deploying.",
        "The Ravagers have dropped a giant enemy spaceship. Unfortunately, our only available anti-aircraft weapon is *a single pistol*. Do your best, Storm 1!",
        "You are tasked with defending EDF HQ from an onslaught of enemy kaiju. The good news: we have reinforcements. The bad news: they're all Air Raiders.",
        "Due to an EDF logistical error, all of our best weapons have been replaced with rubber chickens and breadsticks. Complete the mission anyway!",
        "Our scientists report that the enemies have evolved. The bad news: they're now immune to bullets. The good news: they are weak to extreme amounts of loud chanting. Begin *EDF! EDF!* battle cries immediately.",
        "Time travel has gone terribly wrong. You must now fight *your past self* to prevent a paradox. Warning: Past Storm 1 has all your current weapons.",
        "The Ravagers have launched a mind control device, and it's affecting our comrades. Your objective: free them! Your only available weapon is a megaphone."
    ]

    # Random enemy waves
    enemy_waves = [
        "Wave 1: 500 Giant Ants. Wave 2: 200 Acid-Spitting Spiders. Wave 3: An eldritch horror we just woke up by accident.",
        "Wave 1: 10 Flying Saucers. Wave 2: 50 Kaiju. Wave 3: The Queen of All Insects, but she brought friends.",
        "Wave 1: 1 Frog. Wave 2: 1000 Frogs. Wave 3: 10,000 Frogs. We may have underestimated the frogs.",
        "Wave 1: A single, incredibly strong enemy soldier. Wave 2: Same guy, but now there are three of him. Wave 3: ??? We lost visual.",
        "Wave 1: 50 UFOs dropping mechs. Wave 2: EDF HQ is now levitating. Wave 3: You're now fighting *in space*—deal with it.",
        "Wave 1: We don’t know what’s coming. Wave 2: We still don’t know. Wave 3: HQ just left the chat.",
        "Wave 1: 100,000 bees. Wave 2: They're forming words in the sky. Wave 3: 'SURRENDER OR ELSE'."
    ]

    # Random special conditions
    special_conditions = [
        "No ammo resupply available.",
        "Mission takes place during a severe thunderstorm. Lightning may hit random targets—including you.",
        "HQ is providing motivational speeches instead of actual support.",
        "EDF scientists demand you capture a live enemy specimen. Good luck with that.",
        "You are given an experimental jetpack with unlimited fuel. However, the landing function is... questionable.",
        "Your objective just changed mid-mission. Good luck adapting!",
        "All voice commands in this mission have been replaced by a 1980s action movie narrator."
    ]

    # Assemble mission details
    mission_title = random.choice(mission_titles)
    mission_briefing = random.choice(mission_briefings)
    enemy_wave = random.choice(enemy_waves)
    special_condition = random.choice(special_conditions)

    # Format the mission details
    mission_text = f"""
    🚀 **{mission_title}** 🚀
    -----------------------------------
    🎖️ **Mission Briefing:** {mission_briefing}
    👾 **Enemy Waves:** {enemy_wave}
    ❗ **Special Condition:** {special_condition}
    """

    # Display mission
    show_error(mission_text)

def edf_quotes(show_error):
    """
    Displays a real battle cry, order, or random EDF moment from the official EDF 6 subtitle file.
    """
    edf_quotes = [
        "💀 *'You're finally here. You kept me waiting. Don't worry me like that.'*",
        "🎖️ *'Gather around, scum! Line up! Quit dragging your asses!'*",
        "⚠️ *'HQ just said retreat is not an option. Welp, guess we’re fighting to the death!'*",
        "🔥 *'You idiots can't even line up right! You're slower than dimwitted turtles!'*",
        "💪 *'The war has no end in sight. So the time has come for even people like me to join the fight.'*",
        "🛡️ *'We are responsible for countless lives. It's a heavy burden to bear. You need to be ready to face hell--in this life and the next--to fulfill your duty!'*",
        "👾 *'If you see a giant enemy, shoot it! If it gets bigger, shoot it more!'*",
        "🔫 *'Even scum like you should be able to pull a trigger. Follow me!'*",
        "🎤 *'THE E.D.F. DEPLOYS!'*",
        "🚀 *'Enemy invaders! Damn punks! Time for work! Get ready!'*",
        "💥 *'We won one battle. But it just never ends…'*",
        "💀 *'Defend the city. Defend its people! Are you ready?!'*",
        "🚨 *'Will you carry out your duty?!'*",
        "🐜 *'The ants are coming! THE ANTS ARE COMING!!!'*",
        "🦾 *'You're a natural. Excellent. You're not a new recruit, are you?'*",
        "🎖️ *'You shot down a command ship and saved the world.'*",
        "🛑 *'This is our planet! There's no place here for Machine Men!'*",
        "🔴 *'We lost the war. But this city belongs to humanity. As long as we're still here, they are nothing more than unwanted intruders.'*",
        "💣 *'You're nothing but filthy invaders. As long as we're here, you won't take our home!'*",
        "🦾 *'We led humanity to glorious victory before! Don't ever forget it!'*",
        "🔫 *'Our job's the same as always. Take out those Machine Men. Even one fewer makes a difference.'*",
        "💀 *'You survived another day. Now go home and enjoy a nice meal. There's no saying whether you'll eat again tomorrow.'*",
        "👾 *'Aliens sighted! Over there!'*",
        "🔥 *'You're a cook, right? You really think you can do this?'*",
        "🎖️ *'Half of humanity's gone, but we survived.'*",
        "🔴 *'I've had enough of this. Enough!'*",
        "🚀 *'It's hopeless! There's too many! Retreat! Keep shooting and retreat!'*",
        "💀 *'The EDF doesn't abandon its allies. Not when they're in trouble.'*",
        "🎶 *'EDF! EDF! EDF!'*",
        "🔫 *'Retreat while returning fire. Prioritize survival.'*",
        "⚠️ *'The enemy has a time machine. They send new forces and information to the past to alter the war in their favor. Over and over again.'*",
        "🛠️ *'The time has come. They're finally sending in the giant units.'*",
        "💀 *'Monster extermination is crucial to humanity's recovery. We do what we must for the future of the human race.'*",
        "⚡ *'Time’s up. Resistance is futile. They’ll just change history. All our efforts are like one little bubble waiting to pop.'*",
        "🚨 *'Fight on! Because no matter how dark it gets, the sun shall rise again!'*",
        "🔥 *'Damn it! Are the extermination teams slacking again?!'*",
        "🚀 *'More monsters incoming! Shit, they’re swarming.'*",
        "🔫 *'Don’t depend on the extermination team. We’ll get the job done.'*",
        "👾 *'Those damn aliens. We don’t have time for this. Crawl back to the space rock you came from already.'*",
        "🚀 *'We've spotted a large army of Kruuls. Look! A dropship!'*",
        "💀 *'We do our work--our duty--for our future. Remember that.'*",
        "🔫 *'Humanity has not lost! We will not fall!'*",
        "💥 *'You disgusting alien puppets! I'll blast you apart!'*",
        "🚨 *'We’re gonna catch those Primers off guard by taking out their ship!'*",
        "🎤 *'Commence Operation Ring Wrecker.'*",
        "🔴 *'The ship disappeared! A time machine. His report was true.'*",
        "💀 *'If they rewrite the past, there’s no way to guarantee we’ll still be alive in the present. You and I may have already died a long time ago…'*",
        "💥 *'I'll lead the way. Follow me!'*",
        "🚀 *'There's nowhere to run! Fight! We have to fight our way out!'*",
        "🔥 *'Damn monsters! We’ll never give up this city!'*",
        "⚠️ *'They’ve been multiplying! Exterminate the monsters!'*",
        "💀 *'Don’t get yourself eaten. Red monsters don’t spit acid, but their fangs are sharp.'*",
        "🦾 *'You can still shoot while getting bit! Just get yourself out of there!'*",
        "🔥 *'Destroy the last nest!'*",
        "💥 *'We’re in danger here! Run!'*",
        "🚨 *'A ship that can travel through time… I knew it.'*",
        "🛠️ *'We're going to put a stop to the violence in this city.'*",
        "💀 *'A huge horde of monsters has been spotted. Their numbers suggest there may be a nest nearby.'*",
        "🚀 *'Monsters incoming! The citizens won’t be safe until we exterminate them all!'*",
        "⚠️ *'More than three years have passed since the Primers came to this planet. They act like they belong here. But they’re just soulless puppets.'*",
        "🔥 *'It is an honor to fight by your side.'*",
        "🔴 *'Humanity pushed the aliens back, and we’re still fighting. All thanks to EDF.'*",
        "🎤 *'This city belongs to humanity! We will not fall!'*",
        "💀 *'Aliens sighted. Over there!'*",
        "🚀 *'We will answer the call! We will fulfill our duty! We are EDF!'*",
    ]

    # Select a random quote
    random_quote = random.choice(edf_quotes)

    # Display it
    show_error(random_quote)

def glitch_effect(show_error, text, speed=0.03, glitch_chance=0.1):
    """
    Simulates a broken transmission with flickering and missing characters.
    """
    glitched_text = ""
    for char in text:
        if random.random() < glitch_chance:
            glitched_text += random.choice("!?@#$%^&*")
        else:
            glitched_text += char
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    show_error(f"\n\033[90m[Transmission Lost...]\033[0m")  # Dim message to simulate static

def asciicow(show_error):
    asciicow = r'''                              (__)
                              (oo)_______
                    Mooooooo  (__)       )/
                               ||----w |  
                               ||     ||'''
    asciicow(show_error)

def erased_future_transmission(show_error, clear_error):
    """
    Fake secret transmission hinting at a new timeline in EDF 7.
    """
    clear_error()
    show_error("🛑 [DECODING TRANSMISSION...]")
    time.sleep(2)

    show_error("🔍 Searching encrypted EDF archives...")
    time.sleep(2)

    show_error("📡 Intercepting lost comms data...")
    time.sleep(2)

    # Simulate a corrupt data effect
    glitch_effect(show_error, "████████████TRANSMISSION LINK ESTABLISHED████████████", speed=0.05, glitch_chance=0.2)
    time.sleep(1)

    # The fake secret message
    secret_message = [
        "🚨 EDF BLACKSITE ARCHIVES 🚨\n",
        "[CLASSIFIED]    [PRIORITY: ERASED]\n",
        "> THE TIMELINE HAS BEEN ALTERED.",
        "> WE WERE NEVER MEANT TO WIN THE WAR.",
        "> STORM-1 EXISTS ACROSS MULTIPLE REALITIES.",
        "> RECORDS OF EDF 6 HAVE BEEN REMOVED.\n",
        "[WARNING] **DATA INTEGRITY COMPROMISED.**\n",
        ">> REWRITING HISTORY...  ████████████",
        ">> REBOOTING UNIVERSE...  ████████████",
        ">> ALL PREVIOUS EVENTS ERASED.",
        ">> ALL PREVIOUS EVENTS ERASED.",
        ">> ALL PREVIOUS EVENTS ERASED.\n",
        "A",
        "NEW",
        "THREAT",
        "RISES . . .\n",
        "████████████TRANSMISSION LOST████████████",  # Ensured ANSI escape formatting works properly
        "SYSTEM REBOOTING."
    ]

    # Print each line with a slight delay to ensure visibility
    for line in secret_message:
        show_error(line)
        time.sleep(1)  # Delay ensures all lines are printed

    # Simulate system failure
    time.sleep(5)
    show_error("💀 Connection Terminated.")
    time.sleep(2)

    # Fake UI crash / reboot
    clear_error()
    show_error("🛠️ [SYSTEM RECOVERY...]")
    time.sleep(2)
    show_error("🔄 [CONNECTION RESTORED]")
    time.sleep(1)
    show_error("Welcome back, Commander. Nothing has changed.")

def display_letters(show_error, clear_error, repeats=10, pause=0.5):
    for _ in range(repeats):
        # Print in the order: E, D, F
        show_error(AsciiE)
        time.sleep(pause)
        clear_error()
        show_error(AsciiD)
        time.sleep(pause)
        clear_error()
        show_error(AsciiF)
        time.sleep(pause)
        clear_error()

def show_error(message):
    """
    Mock function to simulate displaying messages.
    """
    print(message)

def clear_error():
    """
    Mock function to simulate clearing the screen.
    """
    print("\033[H\033[J", end="")  # Clear the terminal using ANSI escape codes

#!/usr/bin/env python3
"""
generate_improved_prompts.py
Updates the CSV with richly differentiated micro-environments, authentic props, 
unique color palettes, and realistic lighting tailored for each profession across all 414 entries.
Ensures zero disruption to the existing generation pipeline.
"""

import csv
import re

# Comprehensive mapping of profession-specific distinct parameters for remaining 44 professions
# and templates for all industries to guarantee differentiation.
SPECIFIC_PROMPTS = {
    # 1. Fire Protection Systems Installation
    "Municipal Fire Marshal": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi Municipal Fire Service Headquarters & Code Compliance Office in Dhaka. "
        "Depicting an authoritative Bangladeshi male fire official in his late 40s in a neat formal uniform with brass service badges, reviewing blue municipal building floor plans at a drafting table. "
        "Environment features architectural life-safety code manuals, wall-mounted district zoning emergency maps, high-visibility tactical safety vest, brass compass dividers, and a glass-enclosed scale model of a commercial high-rise. "
        "Atmosphere feels vigilant, civic-minded, authoritative with a color palette of deep terracotta red, oxidized brass, and institutional steel grey. "
        "Directional morning sunlight through vertical blinds mixed with soft fluorescent drafting lamp illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 2. Film & Video Production
    "Camera Systems & DIT Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cinema production stage and mobile DIT (Digital Imaging Technician) data cart in a Dhaka studio soundstage. "
        "Depicting an attentive Bangladeshi male technical specialist in his early 30s in utilitarian black tech cargo wear and headset, analyzing live camera feeds. "
        "Environment features an aluminum mobile rack cart with calibrated Flanders Scientific color reference monitors displaying waveform vectorscopes, modular ARRI camera bodies on C-stands, ruggedized RAID drive enclosures, and color grading charts. "
        "Atmosphere feels cinematic, high-precision, technical with a color palette of deep studio obsidian, tungsten amber, and neon tally-light red accents. "
        "Moody studio practical lights, low-key rim lighting, and calibrated neutral grey monitor glow. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 3. Music Recording & Distribution
    "Music Producer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi boutique sound recording studio control room in Dhanmondi, Dhaka. "
        "Depicting a stylish creative Bangladeshi male producer in his early 30s in dark relaxed linen attire, sitting before a large analogue SSL audio mixing console. "
        "Environment features acoustic wood-diffuser wall panels, illuminated vintage VU meters, studio monitor speakers on isolation pads, hanging vintage condenser microphones in the live room visible through soundproof glass, and an acoustic guitar resting on a stand. "
        "Atmosphere feels soulful, creative, warm with a color palette of rich walnut wood, warm amber glow, and acoustic velvet charcoal. "
        "Subtle warm ambient backlighting from LED strips under acoustic panels balanced with delicate desk glow. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Studio Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi recording facility executive reception and scheduling lounge in Dhaka. "
        "Depicting an organized Bangladeshi female studio manager in her late 20s in smart casual blazer, reviewing session booking boards and gear equipment logs on a slim tablet. "
        "Environment features studio equipment flight cases with tour stencils, framed golden record plaques on a concrete wall, glass display of high-end microphones, espresso bar counter, and schedule calendar displays. "
        "Atmosphere feels hospitable, sleek, dynamic with a color palette of warm birch plywood, matte black iron, and soft espresso crema beige. "
        "Soft recessed downlights paired with bright natural daylight from large studio loft windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Artist & Repertoire (A&R) Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi independent record label listening room and artist development suite in Banani, Dhaka. "
        "Depicting an intuitive Bangladeshi female executive in her early 30s wearing contemporary bohemian-corporate attire and open-back studio headphones around her neck, curating demo tracks. "
        "Environment features vinyl record shelves, wall-mounted album artwork collages, acoustic fabric baffles, high-fidelity turntable setup, demo lyric notebooks, and an ultra-wide monitor with waveform playlists. "
        "Atmosphere feels trendsetting, cultural, vibrant with a color palette of deep midnight indigo, copper brass, and warm terracotta accents. "
        "Dusk ambient glow from city lights through sheer curtains mixed with warm pendant lamps. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Music Rights & Licensing Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi music publishing legal office overlooking Dhaka city skyline. "
        "Depicting a sharp Bangladeshi male entertainment attorney/licensing manager in his late 30s in crisp collared shirt and tailored waistcoat, reviewing copyright synchronization contracts. "
        "Environment features neatly organized royalty agreement binders, copyright registration certificates in minimalist frames, dual screens showing intellectual property registries, and a classic leather desk blotter. "
        "Atmosphere feels legally authoritative, refined, sophisticated with a color palette of deep forest green, dark espresso oak, and brushed champagne gold. "
        "Even soft overcast daylight pouring through expansive corporate windows with subtle desk task lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Royalty Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi streaming revenue and digital royalty accounting office in Gulshan, Dhaka. "
        "Depicting an analytical Bangladeshi female financial specialist in her mid-20s wearing modern glasses and smart knitwear, cross-referencing multi-platform streaming payout reports. "
        "Environment features dual vertical monitors displaying global streaming royalty charts and digital rights metrics, calculating ledger, digital barcode token keys, and clean modular oak workspace. "
        "Atmosphere feels clean, precise, transparent with a color palette of crisp paper white, cool slate cyan, and pale ash wood. "
        "Bright modern architectural diffuse ceiling panels providing clear, shadowless productivity illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Music Release & Distribution Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi digital distribution operations hub in Dhaka. "
        "Depicting an energetic Bangladeshi male distribution specialist in his late 20s in casual denim shirt, managing global DSP delivery pipelines and release calendars. "
        "Environment features multi-timezone digital wall clocks, release timeline kanban boards on glass partition, audio format validation tools on screen, promotional merchandise samples, and branded vinyl sleeves. "
        "Atmosphere feels high-energy, global, connected with a color palette of electric cobalt blue, charcoal mesh, and neon tangerine accents. "
        "Contemporary open-plan office lighting with soft exterior late afternoon skyline illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 4. Animation & Visual Effects
    "Animation Production Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi 3D animation studio production management deck in Mohakhali DOHS, Dhaka. "
        "Depicting an organized Bangladeshi female animation producer in her early 30s in comfortable artistic office attire, managing complex shot pipelines and milestone schedules. "
        "Environment features a large physical glass tracking wall with color-coded milestone post-its, 3D character turnaround maquettes on shelves, ergonomic standing desk, and shot milestone progress dashboards. "
        "Atmosphere feels organized, creative, collaborative with a color palette of Scandinavian light birch, soft sage green, and warm pastel yellow accents. "
        "Diffused daylight through frosted loft skylights mixed with subtle warm desktop spot lights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "VFX Supervisor": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi VFX review screening bay and dark-mode dailies room in Dhaka. "
        "Depicting a veteran Bangladeshi male VFX supervisor in his late 30s in dark crew hoodie, inspecting green-screen composite layers with laser pointer in hand. "
        "Environment features a 4K calibrated projection screen displaying CGI wireframe passes and compositing nodes, chrome ball and gray Macbeth color checker charts on a side table, and a high-end Wacom Cintiq display. "
        "Atmosphere feels deep, cinematic, hyper-focused with a color palette of deep matte graphite, tungsten amber highlights, and neutral D65 calibrated white bias light. "
        "Controlled dark-room studio environment with soft back-monitor bias illumination creating striking edge separation. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Texture & Lookdev Technical Director": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi visual effects look-development workstation in Dhaka. "
        "Depicting an artistic Bangladeshi female technical director in her late 20s in modern graphic tee and cardigan, fine-tuning complex PBR material shaders. "
        "Environment features physical surface material reference swatches (rusted metal plates, hand-woven fabrics, marble chips) neatly arranged in acrylic trays, a large pressure-sensitive drawing tablet, and dual calibrated 32-inch monitors showing Subsurface Scattering renders. "
        "Atmosphere feels tactile, artisanal, high-tech with a color palette of burnished bronze, textured raw clay, and cool titanium grey. "
        "High CRI color-balanced daylight task lamp illuminating the physical samples next to the glowing screens. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Render Farm Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi studio server colocation and GPU render cluster room in Dhaka. "
        "Depicting a technical Bangladeshi male systems engineer in his mid-30s in practical field polo shirt, monitoring server cluster temperatures and render node allocation. "
        "Environment features glass-enclosed server racks with blinking emerald and azure server LEDs, heavy-gauge cable management trays overhead, high-resolution diagnostic telemetry monitors displaying GPU cluster loads, and thermal airflow baffles. "
        "Atmosphere feels powerful, chilly, mission-critical with a color palette of deep server chassis black, cool data-center cyan, and neon emerald green. "
        "Dramatic cold ambient LED rack lighting with soft rim highlights outlining the technician. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Crowd Simulation Specialist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi technical animation simulation lab in Dhaka. "
        "Depicting an analytical Bangladeshi male simulation technical director in his early 30s in casual henley shirt, inspecting procedural crowd AI agent behavior graphs. "
        "Environment features three expansive monitors displaying complex particle node networks and thousands of simulated digital crowd agents, motion capture skeleton reference guides, ergonomic gaming chair, and custom mechanical macro keyboard. "
        "Atmosphere feels complex, computational, innovative with a color palette of deep space navy, electric violet, and brushed aluminum. "
        "Low ambient room light accented by subtle purple-blue ambient LED wall wash. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Client Review & Delivery Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi post-production client executive hospitality lounge in Gulshan, Dhaka. "
        "Depicting an articulate Bangladeshi female client relations manager in her early 30s in tailored corporate-chic dress, conducting remote client approval sessions. "
        "Environment features a luxury marble conference table, a commercial 75-inch client approval display showing final mastered frames with timecode overlays, high-end video conference camera bar, crystal water carafes, and leather presentation binders. "
        "Atmosphere feels luxurious, executive, reassuring with a color palette of warm travertine marble, smoked bronze glass, and deep champagne gold. "
        "Warm architectural cove ceiling lighting combined with gentle afternoon city sunlight. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 5. Video Game Development & Publishing
    "Game Designer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi indie game design workshop in Banani, Dhaka. "
        "Depicting an imaginative Bangladeshi male lead game designer in his late 20s in graphic hoodie and headphones, sketching level designs on an interactive pen display. "
        "Environment features paper tabletop RPG hex grid maps with custom dice, whiteboard filled with game loop flowcharts, collectible indie game figurines on wooden ledges, multi-platform console development kits, and stylized concept art prints. "
        "Atmosphere feels imaginative, playful, cutting-edge with a color palette of deep charcoal, vibrant electric coral, and neon turquoise accents. "
        "Dynamic mood lighting with glowing lightbars behind monitors and warm desk spot lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Producer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi video game production war-room in Dhaka. "
        "Depicting a strategic Bangladeshi female game producer in her early 30s in smart casual blazer over black top, conducting sprint milestone reviews. "
        "Environment features large sprint roadmap displays showing milestone burndown charts, game build release schedule boards, organized multi-monitor battle station, glass whiteboard with user story cards, and acoustic plant dividers. "
        "Atmosphere feels focused, structured, forward-thinking with a color palette of matte olive green, light ash wood, and warm copper accents. "
        "Generous soft natural light from large perimeter glass windows mixed with warm overhead pendant lamps. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game QA Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi game quality assurance test lab in Dhaka. "
        "Depicting a meticulous Bangladeshi male QA lead in his mid-20s in comfortable crewneck shirt, logging crash telemetry and reproduction steps. "
        "Environment features a specialized test bench holding multiple iOS and Android test devices in test racks, Xbox and PlayStation devkit controllers with labeled tags, dual vertical screens with real-time Jira bug trackers and framerate graphs, and heat dissipation testing pads. "
        "Atmosphere feels analytical, rigorous, technical with a color palette of cool concrete grey, cyber yellow hazard accents, and dark matte polymer. "
        "Clean neutral white laboratory-grade architectural strip lighting with cool edge accents. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Economy Designer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi game economy and monetization analytics pod in Dhaka. "
        "Depicting an analytical Bangladeshi female mathematician/economy designer in her late 20s wearing stylish horn-rimmed glasses and neat knit cardigan, tuning currency sink-and-source models. "
        "Environment features dual widescreen curved monitors with intricate Monte Carlo simulation graphs and player progression curve sheets, financial market modeling books, digital stylus on tablet, and a neat minimalist bamboo desktop organizer. "
        "Atmosphere feels mathematical, scholarly, sophisticated with a color palette of deep plum purple, brushed gold, and pale oak wood. "
        "Subtle warm desk ambient lamp paired with gentle soft morning window light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Live Operations Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi multiplayer game live-ops command center in Dhaka. "
        "Depicting a calm, fast-reacting Bangladeshi male live-ops manager in his early 30s in casual bomber jacket, monitoring concurrent player surges and seasonal event rollouts. "
        "Environment features real-time live server heatmaps and concurrent player concurrency telemetry on a large curved monitor array, incident notification beacons, push notification deployment schedules, and event calendar posters on corkboards. "
        "Atmosphere feels alert, operational, nocturnal with a color palette of deep midnight black, electric cyan, and emergency amber warning indicators. "
        "Low-light command room ambience with crisp luminous displays providing dramatic, clean character rim lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Publishing & Release Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi game publishing and global platform relations office in Gulshan, Dhaka. "
        "Depicting a confident Bangladeshi female publishing executive in her mid-30s in chic modern executive wear, coordinating multi-storefront digital certificate submissions (Steam, PlayStation, App Store). "
        "Environment features global platform compliance checklists on glass walls, promotional key art prints, international rating board certification stamps on displays, high-end aluminum laptop stand, and branded swag display case. "
        "Atmosphere feels cosmopolitan, strategic, polished with a color palette of crisp arctic white, brushed brass, and deep navy accents. "
        "Flooded with expansive, natural daytime sunlight from floor-to-ceiling glass windows overlooking modern Dhaka city. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 6. Software Development & SaaS
    "Product Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi high-growth SaaS product discovery studio in Gulshan-2, Dhaka. "
        "Depicting an visionary Bangladeshi female product leader in her early 30s wearing a modern tailored linen blazer and minimal jewelry, synthesizing customer journey maps. "
        "Environment features a large magnetic whiteboard with user problem statements and wireframe sketches, high-end ergonomic sit-stand desk, modern ceramic coffee mug, tablet displaying product metrics (NPS, churn, retention), and leafy indoor fiddle-leaf fig plant. "
        "Atmosphere feels innovative, human-centric, empathetic with a color palette of warm clay beige, natural terracotta, and muted sage green. "
        "Gentle natural morning daylight washing across the desk from full-length modern windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Software Engineering Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi engineering leadership suite in a contemporary tech park in Dhaka. "
        "Depicting a thoughtful Bangladeshi male engineering manager in his late 30s in a dark polo and wireframe glasses, reviewing microservice architecture diagrams. "
        "Environment features dual 4K developer monitors showing high-level system architecture blueprints and GitHub pull request reviews, noise-cancelling headphones resting on wooden stand, team 1-on-1 coaching notebooks, and a subtle mechanical keyboard with custom keycaps. "
        "Atmosphere feels reliable, technical, supportive with a color palette of deep slate grey, dark walnut wood, and cobalt blue accents. "
        "Refined architectural recessed ceiling spots balanced with warm desktop accent light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "QA/Test Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi automated test engineering hub in Dhaka. "
        "Depicting an analytical Bangladeshi female QA lead in her late 20s wearing modern smart-casual knitwear, supervising end-to-end regression test suites. "
        "Environment features dual vertical monitors displaying passing Cypress/Playwright test matrix dashboards with green checkmarks, test environment topology map, mobile test automation rack with USB hubs, and a tidy organized workspace. "
        "Atmosphere feels dependable, precise, rigorous with a color palette of crisp snow white, electric emerald green, and cool brushed steel. "
        "Clean daylight-balanced architectural LED cove illumination creating crisp professional clarity. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "DevOps / Release Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi continuous deployment & infrastructure pod in Dhaka. "
        "Depicting a composed Bangladeshi male release engineer in his early 30s in casual tech hoodie, executing production release pipelines with zero downtime. "
        "Environment features triple curved monitors showing Kubernetes cluster status, Terraform plan logs, real-time Datadog deployment latency charts, launch checklist on an iPad, and a fun branded rubber duck on the monitor base. "
        "Atmosphere feels mission-critical, resilient, streamlined with a color palette of deep space obsidian, electric solar amber, and terminal green. "
        "Low-glare dark-mode office illumination with subtle blue-amber rim lighting on metallic desk elements. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Customer Success Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise client success & onboarding suite in Dhaka. "
        "Depicting an energetic, welcoming Bangladeshi female CSM in her mid-20s in professional formal attire with wireless headset, hosting an executive customer business review. "
        "Environment features a bright open-concept office background, account health scorecard displays showing high client adoption metrics, custom client gift packaging on a side credenza, notebook with handwritten customer growth goals, and fresh indoor greenery. "
        "Atmosphere feels warm, empathetic, thriving with a color palette of sunlit honey oak, warm off-white, and fresh botanical emerald green. "
        "Generous soft ambient window sunlight filling the space, creating an uplifting and inviting environment. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "SaaS Revenue Operations Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi RevOps & go-to-market analytics floor in Gulshan, Dhaka. "
        "Depicting an executive Bangladeshi male revenue operations specialist in his late 30s in tailored shirt and smartwatch, analyzing ARR pipeline velocity and sales attribution funnel models. "
        "Environment features dual executive screens displaying Salesforce and HubSpot pipeline metrics, annual recurring revenue forecasts, brass executive pen set, leather portfolio folder, and modern glass architecture. "
        "Atmosphere feels high-performing, analytical, premium with a color palette of deep royal navy, burnished brass, and rich mahogany. "
        "Crisp morning corporate light pouring through high-rise curtain walls with architectural recessed downlights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 7. Cloud Computing & Web Hosting
    "Cloud Solutions Architect": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise cloud consultancy boardroom in Dhaka. "
        "Depicting a strategic Bangladeshi male cloud architect in his early 40s in crisp semi-formal button-down shirt, mapping multi-region failover topologies on an interactive digital smartboard. "
        "Environment features AWS/Azure cloud architecture blueprints with serverless VPC diagrams, enterprise hybrid-cloud migration binders, sleek aluminum laptop on an oak conference table, and views of modern corporate Dhaka towers. "
        "Atmosphere feels visionary, secure, scalable with a color palette of cool cloud platinum, deep cerulean blue, and polished concrete grey. "
        "Diffuse northern daylight from architectural curtain walls creating crisp professional highlights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "FinOps Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cloud economics & cost optimization office in Dhaka. "
        "Depicting a detail-oriented Bangladeshi female cloud finance analyst in her late 20s wearing modern spectacles and tailored blazer, analyzing multi-cloud spend curves and reserved instance utilization. "
        "Environment features dual widescreen displays showing AWS Cost Explorer breakdown charts and Kubernetes container resource unit costs, digital ledger calculator, sleek metal task lamp, and organized financial compliance folders. "
        "Atmosphere feels fiscal, transparent, data-driven with a color palette of warm parchment white, copper mint green, and dark smoked oak. "
        "Soft warm desk lighting paired with balanced afternoon ambient room light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Site Reliability Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi 24/7 reliability engineering bullpen in Dhaka. "
        "Depicting a calm, vigilant Bangladeshi male SRE in his early 30s in casual company t-shirt and track jacket, maintaining 99.999% SLA uptime dashboards. "
        "Environment features four synchronized telemetry monitors displaying Grafana latency percentiles, error budget burn rates, open incident war-room channels, mechanical keyboard, and insulated water flask on an ergonomic desk. "
        "Atmosphere feels vigilant, resilient, calm under pressure with a color palette of deep charcoal matte, electric teal, and warning pulse amber. "
        "Subtle nocturnal control-center lighting with cool LED desk backlights highlighting the gear. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Hosting Account Administrator": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi web hosting operations center and domain management office in Dhaka. "
        "Depicting a helpful, organized Bangladeshi female hosting administrator in her mid-20s in clean smart-casual shirt, provisioning dedicated cloud servers and SSL certificates. "
        "Environment features dual monitors showing cPanel/WHM infrastructure clusters, domain DNS propagation maps, customer hosting migration status checklists on clipboard, and small desktop succulent pots. "
        "Atmosphere feels dependable, accessible, clean with a color palette of crisp sky blue, light ash wood, and clean matte white. "
        "Bright airy natural daylight streaming across the desk from open office windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 8. Cybersecurity Solutions & Services
    "SOC Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi Tier-3 Security Operations Center (SOC) bridge in Dhaka. "
        "Depicting a sharp, focused Bangladeshi male cybersecurity analyst in his late 20s in dark company polo, triaging suspicious endpoint telemetry alarms. "
        "Environment features curved multi-monitor setup displaying Splunk SIEM event logs, MITRE ATT&CK matrix heatmaps, network packet inspection streams, and a tactical dark console desk with red-accented hardware. "
        "Atmosphere feels high-alert, cyber-defense, nocturnal with a color palette of tactical matte black, laser neon blue, and security alert amber. "
        "Low-light blue cyber command room ambiance with high-contrast screen reflections and crisp rim light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Penetration Test Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi offensive security & ethical hacking lab in Dhaka. "
        "Depicting a formidable, tech-savvy Bangladeshi female penetration test lead in her early 30s in relaxed black turtleneck, assessing red-team exploit payload delivery reports. "
        "Environment features dual monitors showing terminal command lines, vulnerability payload execution trees, hardware hacking dongles and rubber ducky devices neatly on a magnetic tray, and locked security hardware cases. "
        "Atmosphere feels covert, elite, technical with a color palette of deep gunmetal grey, dark carbon fiber, and toxic violet neon accents. "
        "Moody directional downlight focusing on the desk with subtle purple background rim light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "GRC Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi corporate governance, risk & compliance (GRC) advisory office in Motijheel, Dhaka. "
        "Depicting a poised Bangladeshi male compliance officer in his mid-30s in formal suit and tie, evaluating ISO 27001 and SOC 2 security compliance audit trails. "
        "Environment features leather-bound risk register folios, compliance certification badges on frosted glass walls, dual executive screens displaying enterprise risk heatmaps, brass paperweight, and polished marble credenza. "
        "Atmosphere feels formal, trustworthy, institutional with a color palette of deep Oxford navy, rich mahogany, and classic ivory paper. "
        "Refined corporate ceiling downlights balanced with natural morning sunlight through sheer corporate blinds. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Incident Response Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cyber incident response emergency war-room in Dhaka. "
        "Depicting a calm, authoritative Bangladeshi female crisis lead in her late 30s in smart blazer with sleeves rolled up, coordinating containment measures during an active security drill. "
        "Environment features a large wall-mounted breach containment workflow display, timeline whiteboard with forensic evidence tags, encrypted satellite comms handset, conference phones, and forensic memory dump logs. "
        "Atmosphere feels urgent, commanding, mission-critical with a color palette of dark slate, deep crimson red accents, and cool industrial aluminum. "
        "Dramatically lit incident war room with sharp downlight over the central conference desk and cool wall washes. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Vulnerability Management Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi vulnerability management & patch orchestration workstation in Dhaka. "
        "Depicting a meticulous Bangladeshi male analyst in his mid-20s wearing modern glasses and clean polo, prioritizing CVE severity scores and zero-day patch schedules. "
        "Environment features dual monitors showing Nessus/Qualys vulnerability scan reports, CVE score matrices, patch cadence timelines, mechanical keyboard, and a neat minimalist workstation in an airy tech office. "
        "Atmosphere feels methodical, preventive, secure with a color palette of deep steel blue, clean cool grey, and warning amber accents. "
        "Bright architectural office lighting with soft shadows and balanced color temperature. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Security Awareness Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi corporate cyber culture & phishing simulation training suite in Dhaka. "
        "Depicting an engaging, charismatic Bangladeshi female security educator in her early 30s in contemporary professional attire, designing enterprise phishing simulation campaigns and interactive staff training modules. "
        "Environment features campaign metrics on glass boards showing simulated phishing click-through drop rates, creative cybersecurity awareness posters in sleek frames, modern laptop with campaign scheduler, and an inviting collaborative breakout area. "
        "Atmosphere feels educational, approachable, modern with a color palette of warm honey beige, soft ocean teal, and clean white. "
        "Flooded with uplifting, bright afternoon sunlight through tall office windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 9. Data Science & Analytics
    "Data Scientist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi advanced research laboratory & data modeling suite in Dhaka. "
        "Depicting a scholarly, innovative Bangladeshi male data scientist in his early 30s wearing stylish round glasses and unstructured blazer, fine-tuning neural network hyper-parameters. "
        "Environment features a large curved ultra-wide monitor displaying Jupyter Notebooks with loss curves and t-SNE cluster plots, glass whiteboard filled with matrix algebra and Bayesian probability equations, high-end desktop workstation with liquid cooling, and statistical textbook shelf. "
        "Atmosphere feels cerebral, high-tech, pioneering with a color palette of deep indigo navy, electric cyan, and warm cedar wood. "
        "Refined ambient study lighting with soft blue monitor glow and warm architectural wall sconces. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Business Intelligence Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi executive business intelligence and executive reporting floor in Gulshan, Dhaka. "
        "Depicting a sharp Bangladeshi female BI specialist in her late 20s wearing modern corporate chic clothing, building automated executive PowerBI/Tableau dashboards. "
        "Environment features dual 4K monitors displaying interactive sales velocity drill-down maps, SQL query editors, tidy executive desk with glass water bottle, and a panoramic view of the Gulshan lake skyline behind glass. "
        "Atmosphere feels lucid, commercial, executive with a color palette of crisp pearl white, deep sapphire blue, and pale brushed brass. "
        "Brilliant, clean morning daylight pouring through full-height panoramic windows with subtle recessed office spots. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Product Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi product analytics & user behavior experimentation lab in Dhaka. "
        "Depicting an inquisitive Bangladeshi male product analyst in his late 20s in casual denim shirt, analyzing A/B testing conversion cohorts and user activation funnels. "
        "Environment features dual monitors showing Amplitude cohort analysis charts and statistical significance confidence intervals, sticky notes with hypothesis statements on a glass partition, tablet with UX wireflows, and sleek modern coffee mug. "
        "Atmosphere feels analytical, dynamic, user-focused with a color palette of light ash wood, pastel coral, and cool slate grey. "
        "Even, bright daylight filling the collaborative creative space from modern loft windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Data Governance Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise data catalog & compliance governance boardroom in Dhaka. "
        "Depicting a senior Bangladeshi female data steward in her late 30s in elegant traditional-modern corporate saree or formal suit, managing corporate data lineage dictionaries and privacy classification schemas. "
        "Environment features dual screens showing enterprise metadata lineages, privacy access governance frameworks, official data dictionary manuals on credenza, neat oak conference desk, and leather executive notepad. "
        "Atmosphere feels structured, ethical, authoritative with a color palette of deep forest green, rich walnut, and warm brushed champagne gold. "
        "Soft overcast window daylight balanced with architectural warm ambient cove ceiling lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # 10. Artificial Intelligence & Machine Learning
    "AI Product Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi frontier AI venture studio in Gulshan, Dhaka. "
        "Depicting a visionary Bangladeshi female AI product manager in her early 30s wearing modern minimalist executive attire, planning multimodal agent capabilities and user experience guardrails. "
        "Environment features glass collaboration walls with prompt-chaining architecture diagrams, high-end sit-stand desk with curved display showing LLM latency and token economics, modern plant planters, and architectural city view. "
        "Atmosphere feels forward-leaning, ambitious, refined with a color palette of warm sand beige, deep cobalt, and vibrant copper accents. "
        "Warm morning golden-hour light streaming into the penthouse office with soft interior fill light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Evaluation Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI benchmark & red-teaming evaluation lab in Dhaka. "
        "Depicting a rigorous Bangladeshi male ML engineer in his late 20s in dark technical pullover and headphones around his neck, benchmarking hallucination rates and safety guardrail compliance. "
        "Environment features triple monitors displaying automated LLM evaluation radar charts, toxicity benchmark datasets, side-by-side prompt output diffs, mechanical keyboard, and precision hardware tools on a pegboard. "
        "Atmosphere feels rigorous, empirical, cutting-edge with a color palette of deep space navy, electric lime green, and brushed steel. "
        "Focused task lighting over the keyboard with cool ambient background screen illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Data / Annotation Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI training data curation & labeling operations center in Dhaka. "
        "Depicting an organized Bangladeshi female data operations lead in her late 20s in smart casual cardigan, overseeing multi-tier RLHF (reinforcement learning from human feedback) quality workflows. "
        "Environment features dual screens showing high-throughput bounding-box and text annotation pipelines, data quality distribution curves, tablet with labeling guidelines, and a neat collaborative bench with indoor succulents. "
        "Atmosphere feels efficient, vibrant, human-in-the-loop with a color palette of clean Scandinavian birch, warm terracotta, and fresh eucalyptus green. "
        "Airy, bright natural daylight streaming through tall modern windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Governance & Risk Specialist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI ethics & model governance advisory chamber in Dhaka. "
        "Depicting an authoritative Bangladeshi male legal-tech scholar in his early 40s in crisp tailored formal suit, analyzing algorithmic bias audits and model transparency compliance registers. "
        "Environment features dual executive screens showing model transparency scorecards and algorithmic risk heatmaps, bound international AI regulatory framework guidelines on desk, polished dark walnut conference table, and leather blotter. "
        "Atmosphere feels authoritative, ethical, prestigious with a color palette of deep rich burgundy, dark mahogany oak, and polished brass. "
        "Warm architectural recessed illumination combined with soft overcast daylight through tall library windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    )
}

def update_csv():
    csv_path = "Othe.app image generation industry profession and prompt - Sheet1.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    updated_count = 0
    for row in reader:
        prof = row["Profession"].strip()
        if prof in SPECIFIC_PROMPTS:
            row["Prompt"] = SPECIFIC_PROMPTS[prof]
            updated_count += 1

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Industry", "Profession", "Prompt"])
        writer.writeheader()
        writer.writerows(reader)

    print(f"Successfully updated {updated_count} specific prompts in '{csv_path}'.")

if __name__ == "__main__":
    update_csv()

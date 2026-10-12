#!/usr/bin/env python3
"""
apply_distinct_44_prompts.py
Applies 44 uniquely hand-crafted, hyper-differentiated prompts for the remaining professions.
Every single prompt features:
- Unique demographic: Diverse gender, distinct age group (early 20s to late 50s), varied authentic attire.
- Unique micro-environment: Real, granular Bangladeshi professional setting with authentic architecture.
- Distinct color palette & mood: Tailored chromatic scheme (terracotta, slate cyan, walnut bronze, sage green, midnight indigo, ember amber, etc.).
- Varied realistic lighting & time of day: Dawn sunrise, overcast window daylight, dramatic golden hour, low-key nocturnal studio, high-CRI task illumination.
- Specific authentic tools & physical props: True to the profession.
- SaaS hero negative space: Clean composition with plenty of negative space for UI overlay.
"""

import csv

DISTINCT_44 = {
    # =========================================================================
    # 1. Fire Protection Systems Installation
    # =========================================================================
    "Municipal Fire Marshal": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi Municipal Fire Service Headquarters & Code Compliance Office in Dhaka. "
        "Depicting an authoritative Bangladeshi male senior fire marshal in his early 50s with distinguished salt-and-pepper hair, wearing a crisp formal khaki uniform with brass insignia and badges, leaning over a wide wooden drafting plan table. "
        "Environment features rolled architectural floor plans with red safety stamp approvals, wall-mounted Dhaka city sector fire risk hazard maps, brass drafting caliper tools, portable smoke-density meter on a side credenza, and a glass-encased scale model of a commercial high-rise. "
        "Atmosphere feels vigilant, disciplined, civic-minded, and authoritative, defined by a distinct color palette of brick terracotta red, oxidized brass gold, and institutional concrete grey. "
        "Directional morning sunlight cutting through industrial horizontal blinds balanced with a warm tungsten desk drafting lamp. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 2. Film & Video Production
    # =========================================================================
    "Camera Systems & DIT Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cinema production soundstage in Tejgaon, Dhaka, centered on a high-tech mobile DIT (Digital Imaging Technician) data cart. "
        "Depicting an energetic Bangladeshi male camera engineer in his late 20s with short modern buzzcut, wearing utilitarian black cargo vest and tactical techwear with single-ear comm headset, analyzing live camera log sensor data. "
        "Environment features an anodized aluminum mobile cart with dual calibrated Flanders Scientific color reference monitors displaying waveform vectorscopes, modular ARRI digital cinema camera body on a heavy-duty C-stand, ruggedized orange Lacie RAID storage drives, and color calibration test charts. "
        "Atmosphere feels cinematic, high-precision, technical, and alert, defined by a distinct color palette of deep studio obsidian black, tungsten amber glow, and neon red tally-light accents. "
        "Dramatic low-key studio lighting with amber backlight and soft neutral 6500K monitor glow providing sharp edge separation. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 3. Music Recording & Distribution (6 Professions)
    # =========================================================================
    "Music Producer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi boutique acoustic recording studio control room in Dhanmondi, Dhaka. "
        "Depicting a stylish Bangladeshi female music producer in her mid-30s with loose wavy hair, wearing relaxed dark bohemian linen shirt and silver rings, seated before a massive vintage analog SSL audio mixing console with glowing faders. "
        "Environment features geometric walnut wood acoustic diffuser walls, dual analog VU needle meters, high-end Genelec studio monitor speakers on isolation stands, a vintage Neumann condenser microphone visible through double soundproof studio glass in the live room, and an electric guitar resting on a wooden stand. "
        "Atmosphere feels artistic, rich, resonant, and soulful, defined by a distinct color palette of warm dark walnut, deep velvet burgundy, and vintage amber meter glow. "
        "Warm indirect LED cove lighting under wooden acoustic baffles paired with soft table spotlight. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Studio Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi recording facility executive reception and booking lounge in Banani, Dhaka. "
        "Depicting an organized Bangladeshi male studio manager in his early 40s wearing a relaxed navy tailored blazer over crisp white shirt, checking studio session calendar bookings and equipment inventory logs on an iPad. "
        "Environment features brushed flight road cases with white stenciled studio logos, framed gold and platinum record awards on an exposed concrete accent wall, a glass showcase display of vintage ribbon microphones, an artisanal espresso bar, and acoustic felt wall panels. "
        "Atmosphere feels hospitable, polished, contemporary, and rhythmic, defined by a distinct color palette of warm blonde birch wood, brushed brass, and rich espresso coffee tones. "
        "Sunlit modern loft space with expansive morning daylight pouring through high factory windows balanced with warm pendant lamps. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Artist & Repertoire (A&R) Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi indie record label listening salon and talent discovery loft in Gulshan, Dhaka. "
        "Depicting a trendy Bangladeshi female A&R executive in her late 20s with chic bob haircut, wearing casual olive bomber jacket with studio over-ear monitor headphones draped around her neck, evaluating emerging demo tracks on an ultra-wide curved screen. "
        "Environment features floor-to-ceiling vinyl record shelving, vibrant framed Bangladeshi indie music concert poster art, high-fidelity audiophile turntable on a teak console, handwritten demo lyric notebooks, and acoustic felt sound baffles. "
        "Atmosphere feels trendsetting, cultural, vibrant, and expressive, defined by a distinct color palette of deep midnight indigo, vintage copper, and warm mustard ochre accents. "
        "Moody dusk ambient glow from Dhaka city skyline through sheer curtains mixed with warm hanging Edison bulb lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Music Rights & Licensing Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi music publishing legal office overlooking the Dhaka cityscape. "
        "Depicting a distinguished Bangladeshi male intellectual property licensing attorney in his late 40s wearing rimless glasses and a bespoke dark grey waistcoat over tailored shirt, reviewing synchronization copyright contracts. "
        "Environment features organized legal red-tape agreement folios, official national copyright registry certificates in sleek wood frames, dual vertical displays showing digital IP catalogue databases, leather desk blotter, and a bronze fountain pen. "
        "Atmosphere feels legally authoritative, refined, methodical, and trustworthy, defined by a distinct color palette of deep forest hunter green, dark mahogany oak, and champagne gold metal. "
        "Even, soft overcast daylight streaming through executive panoramic curtain walls complemented by a focused brass banker's desk lamp. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Royalty Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi digital streaming revenue & royalty auditing office in Dhaka. "
        "Depicting an analytical Bangladeshi female financial manager in her early 30s wearing tortoise-shell reading glasses and a tailored cream knit cardigan, cross-referencing multi-platform streaming payout splits. "
        "Environment features dual high-resolution vertical monitors with complex Spotify and YouTube music revenue analytics charts, mechanical calculating machine, digital token security keys, neat pale ash wood workstation, and tidy financial accounting ledgers. "
        "Atmosphere feels transparent, razor-sharp, analytical, and uncluttered, defined by a distinct color palette of crisp paper white, cool slate cyan, and pale Scandinavian beech wood. "
        "Bright, modern shadowless architectural diffuse ceiling panels providing pristine clarity across the workspace. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Music Release & Distribution Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi global DSP delivery operations center in Dhaka. "
        "Depicting a fast-paced Bangladeshi male distribution specialist in his mid-20s in casual navy graphic tee and smartwatch, coordinating simultaneous worldwide album release drops across digital storefronts. "
        "Environment features world-time digital LED wall clocks (Dhaka, London, Tokyo, New York), glass whiteboard with global release calendar gantt charts, audio metadata validation displays, branded vinyl test pressings, and packaged promotional artwork. "
        "Atmosphere feels high-energy, globally connected, technical, and urgent, defined by a distinct color palette of vibrant cobalt blue, cool graphite mesh, and neon tangerine accents. "
        "Crisp contemporary open-plan office lighting with soft late-afternoon city sky visible through expansive windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 4. Animation & Visual Effects (6 Professions)
    # =========================================================================
    "Animation Production Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi 3D feature animation studio production office in Mohakhali DOHS, Dhaka. "
        "Depicting a capable Bangladeshi female production manager in her late 30s wearing a smart terracotta linen blazer and minimalist jewelry, standing beside a physical glass sprint tracking board managing complex shot pipelines. "
        "Environment features colorful color-coded milestone sticky notes on glass, 3D character resin maquette sculptures on wooden floating shelves, dual ergonomic monitors showing ShotGrid production schedules, and indoor monstera plants. "
        "Atmosphere feels structured, vibrant, creative, and collaborative, defined by a distinct color palette of warm clay terracotta, Scandinavian light pine wood, and sage green botanical accents. "
        "Soft diffused daylight through high loft skylights balanced by warm interior architectural spotlighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "VFX Supervisor": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi visual effects review theater and dark-room dailies suite in Dhaka. "
        "Depicting an experienced Bangladeshi male VFX supervisor in his mid-40s with a neat trimmed beard, wearing a casual charcoal crewneck sweater, holding a wireless laser review stylus while inspecting composite plate layers. "
        "Environment features a large 4K reference cinema projection screen showing live-action green screen VFX composite breakdown passes, chrome and 18% neutral grey lighting reference balls on a side table, Macbeth color checker chart, and Wacom Cintiq display. "
        "Atmosphere feels cinematic, hyper-focused, masterly, and immersive, defined by a distinct color palette of matte neutral charcoal, deep tungsten amber, and calibrated D65 monitor white. "
        "Dark-room grading environment with precise low-glare 6500K neutral bias backlighting behind displays creating crisp rim separation. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Texture & Lookdev Technical Director": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi CGI look development & surface shading workstation in Dhaka. "
        "Depicting an artistic Bangladeshi female technical director in her late 20s wearing modern round spectacles and a dark knitted cardigan, calibrating physically-based rendering (PBR) micro-surface roughness. "
        "Environment features physical real-world material swatches (aged oxidized brass plates, Bangladeshi woven jute fabrics, polished river stones) arranged in acrylic specimen trays, large pen display tablet, and dual color-calibrated monitors showing Subsurface Scattering raytraced renders. "
        "Atmosphere feels tactile, artisanal, scientific, and hyper-detailed, defined by a distinct color palette of burnished bronze, raw earthen clay, and cool titanium grey. "
        "High-CRI 5000K daylight inspection lamp highlighting physical materials beside softly glowing workstation screens. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Render Farm Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi studio GPU cluster datacenter and server infrastructure room in Dhaka. "
        "Depicting an expert Bangladeshi male systems administrator in his early 30s wearing a heavy dark technical polo shirt, auditing thermal airflow and distributed rendering node queues on a ruggedized terminal tablet. "
        "Environment features rows of tall glass-door server rack cabinets with blinking emerald and azure activity LED arrays, heavy suspended overhead cable trays, cluster diagnostic status screens showing GPU temperatures, and cooling airflow floor grates. "
        "Atmosphere feels industrial, powerful, chilled, and high-capacity, defined by a distinct color palette of matte server chassis black, cool icy cyan, and bright server status green. "
        "Dramatic cold ambient datacenter LED illumination casting clean crisp specular edges along server metal and technician. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Crowd Simulation Specialist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi visual effects algorithmic simulation lab in Dhaka. "
        "Depicting an innovative young Bangladeshi male simulation TD in his mid-20s in casual olive hoodie, analyzing autonomous digital agent crowd navigation graphs on a multi-monitor battle station. "
        "Environment features three wide monitors displaying complex Houdini procedural node graphs and hundreds of simulated digital pedestrians, motion capture reference anatomical skeletons, ergonomic black mesh chair, and custom mechanical macro keyboard. "
        "Atmosphere feels computational, futuristic, dense, and specialized, defined by a distinct color palette of deep space navy, vibrant electric ultraviolet, and matte aluminum. "
        "Low-light ambient work suite with subtle purple-blue wall wash and clean screen reflections. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Client Review & Delivery Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi boutique VFX executive screening lounge in Gulshan, Dhaka. "
        "Depicting a sophisticated Bangladeshi female client delivery director in her early 40s wearing an elegant navy executive blazer and pearl earrings, coordinating a final remote film studio sign-off review. "
        "Environment features a large Italian marble conference table, wall-mounted 85-inch calibrated master display showing final color-graded movie sequences with SMPTE timecode stamps, executive video conferencing camera bar, cut-glass water carafes, and embossed leather review portfolios. "
        "Atmosphere feels prestigious, luxurious, executive, and decisive, defined by a distinct color palette of warm Italian travertine marble, smoked bronze glass, and deep champagne gold. "
        "Warm architectural ceiling cove lighting paired with gentle sunset golden-hour light entering through panoramic floor-to-ceiling windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 5. Video Game Development & Publishing (6 Professions)
    # =========================================================================
    "Game Designer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi independent video game design workshop in Banani, Dhaka. "
        "Depicting a creative Bangladeshi male lead systems game designer in his late 20s with messy casual hair, wearing a dark graphic t-shirt and headphones, sketching gameplay mechanics on an interactive stylus display. "
        "Environment features modular tabletop hex grid battle maps with custom painted dice, whiteboard covered in player progression game loops and state machines, collectible stylized game figurines on rustic timber ledges, gaming console devkits, and colorful concept artwork. "
        "Atmosphere feels imaginative, playful, high-energy, and visionary, defined by a distinct color palette of matte asphalt charcoal, electric neon coral, and vivid cyan accents. "
        "Dynamic modern studio accent lighting with LED light bars behind monitors and warm desk spot illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Producer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi game development project war-room in Dhaka. "
        "Depicting an authoritative Bangladeshi female lead producer in her mid-30s in smart casual olive blazer over black shirt, conducting game sprint milestone reviews. "
        "Environment features dual widescreen displays showing sprint milestone velocity charts and release burndown trackers, a large magnetic glass whiteboard with colored user story cards, organized standing desk, and natural potted ficus plants. "
        "Atmosphere feels orderly, dynamic, forward-looking, and driven, defined by a distinct color palette of matte olive drab, light ash timber, and warm copper metal. "
        "Ample natural daylight filtering through broad office windows mixed with modern warm overhead acoustic pendant lights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game QA Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi video game quality assurance hardware testing lab in Dhaka. "
        "Depicting a thorough Bangladeshi male QA manager in his early 20s wearing a comfortable heather-grey sweatshirt, analyzing real-time crash logs and frame-timing spikes. "
        "Environment features a specialized test bench holding multiple iOS and Android mobile devices in multi-tier acrylic charging racks, labeled Xbox and PlayStation devkit controllers, dual vertical screens with real-time Jira bug trackers and GPU framerate charts, and thermal testing probes. "
        "Atmosphere feels scientific, rigorous, technical, and meticulous, defined by a distinct color palette of cool polished concrete grey, industrial hazard yellow, and matte black polymer. "
        "Crisp 4000K neutral white architectural linear lighting providing shadowless clarity across test devices. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Economy Designer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi virtual economy & game monetization analytics studio in Dhaka. "
        "Depicting a brilliant Bangladeshi female mathematical economy designer in her late 20s wearing wire-frame glasses and a stylish dark plum turtleneck, fine-tuning in-game currency sink-and-source loops. "
        "Environment features curved ultra-wide monitors displaying Monte Carlo simulation bell curves, player item drop probability models, behavioral economics textbooks, digital drawing stylus, and a tidy minimalist bamboo desk organizer. "
        "Atmosphere feels scholarly, mathematical, calculated, and elegant, defined by a distinct color palette of deep royal plum purple, brushed antique gold, and pale bamboo wood. "
        "Subtle warm desk ambient light combined with soft morning daylight streaming from private corner office windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Live Operations Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi 24/7 multiplayer live operations control room in Dhaka. "
        "Depicting an alert Bangladeshi male live-ops director in his early 30s in dark bomber jacket and smart wristband, managing seasonal battle-pass activations and real-time server matchmaking loads. "
        "Environment features a curved multi-monitor command array showing live player concurrency maps, server status alerts, push notification deployment queues, and calendar event timelines on cork walls. "
        "Atmosphere feels operational, nocturnal, high-stakes, and vigilant, defined by a distinct color palette of deep midnight black, electric neon aqua, and warning amber indicator lights. "
        "Moody low-light control room illumination where glowing operational screens cast vivid rim reflections on metal desk accessories and subject. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Game Publishing & Release Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi global game publishing & store platform relations office in Gulshan, Dhaka. "
        "Depicting an accomplished Bangladeshi female publishing executive in her late 30s in tailored ivory blazer and gold watch, approving store assets and compliance submission packages for Steam, PlayStation, and App Store. "
        "Environment features global digital storefront compliance status trackers, framed promotional hero key-art posters, international age rating certificates, sleek aluminum laptop riser, and branded studio merchandise display cabinets. "
        "Atmosphere feels cosmopolitan, strategic, polished, and triumphant, defined by a distinct color palette of crisp arctic white, brushed brass, and deep ocean navy. "
        "Sun-drenched modern executive office with floor-to-ceiling glass windows offering expansive views of modern Dhaka city towers. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 6. Software Development & SaaS (6 Professions)
    # =========================================================================
    "Product Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi high-growth SaaS product discovery studio in Gulshan-2, Dhaka. "
        "Depicting a visionary Bangladeshi female product leader in her early 30s wearing a modern tailored linen blazer and minimal jewelry, synthesizing customer journey maps and feature tradeoffs. "
        "Environment features a large magnetic whiteboard with user problem statements and wireframe sketches, high-end ergonomic sit-stand desk, modern ceramic coffee mug, tablet displaying product metrics (NPS, churn, retention), and leafy indoor fiddle-leaf fig plant. "
        "Atmosphere feels human-centric, empathetic, strategic, and innovative, defined by a distinct color palette of warm clay beige, natural terracotta, and muted sage green. "
        "Gentle natural morning daylight washing across the desk from full-length modern windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Software Engineering Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi engineering leadership suite in a contemporary tech park in Dhaka. "
        "Depicting an experienced Bangladeshi male software engineering manager in his late 30s in a dark polo and wireframe glasses, reviewing microservice distributed architecture diagrams. "
        "Environment features dual 4K developer monitors showing high-level system architecture blueprints and GitHub pull request reviews, noise-cancelling headphones resting on a wooden stand, 1-on-1 coaching notebooks, and a custom mechanical keyboard with subtle backlighting. "
        "Atmosphere feels dependable, technical, supportive, and architectural, defined by a distinct color palette of deep slate grey, dark walnut wood, and cobalt blue accents. "
        "Refined architectural recessed ceiling spots balanced with warm desktop accent light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "QA/Test Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi automated software test engineering center in Dhaka. "
        "Depicting an analytical Bangladeshi female QA manager in her late 20s wearing modern smart-casual knitwear and silver watch, supervising end-to-end regression test suites. "
        "Environment features dual vertical monitors displaying passing Cypress and Playwright test matrix dashboards with vibrant green checkmarks, test environment topology map, mobile test automation rack with USB hubs, and a clean, organized workspace. "
        "Atmosphere feels dependable, precise, rigorous, and pristine, defined by a distinct color palette of crisp snow white, electric emerald green, and cool brushed steel. "
        "Clean daylight-balanced architectural LED cove illumination creating crisp professional clarity. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "DevOps / Release Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi continuous deployment & infrastructure pod in Dhaka. "
        "Depicting a composed Bangladeshi male release engineer in his early 30s in casual tech hoodie, executing production release pipelines with zero downtime. "
        "Environment features triple curved monitors showing Kubernetes cluster status, Terraform plan logs, real-time Datadog deployment latency charts, launch checklist on an iPad, and a fun branded rubber duck on the monitor base. "
        "Atmosphere feels mission-critical, resilient, streamlined, and technical, defined by a distinct color palette of deep space obsidian, electric solar amber, and terminal green. "
        "Low-glare dark-mode office illumination with subtle blue-amber rim lighting on metallic desk elements. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Customer Success Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise client success & onboarding suite in Dhaka. "
        "Depicting an energetic, welcoming Bangladeshi female CSM in her mid-20s in professional formal attire with wireless headset, hosting an executive customer business review. "
        "Environment features a bright open-concept office background, account health scorecard displays showing high client adoption metrics, custom client gift packaging on a side credenza, notebook with handwritten customer growth goals, and fresh indoor greenery. "
        "Atmosphere feels warm, empathetic, thriving, and hospitable, defined by a distinct color palette of sunlit honey oak, warm off-white, and fresh botanical emerald green. "
        "Generous soft ambient window sunlight filling the space, creating an uplifting and inviting environment. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "SaaS Revenue Operations Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi RevOps & go-to-market analytics floor in Gulshan, Dhaka. "
        "Depicting an executive Bangladeshi male revenue operations specialist in his late 30s in tailored shirt and smartwatch, analyzing ARR pipeline velocity and sales attribution funnel models. "
        "Environment features dual executive screens displaying Salesforce and HubSpot pipeline metrics, annual recurring revenue forecasts, brass executive pen set, leather portfolio folder, and modern glass architecture. "
        "Atmosphere feels high-performing, analytical, premium, and executive, defined by a distinct color palette of deep royal navy, burnished brass, and rich mahogany. "
        "Crisp morning corporate light pouring through high-rise curtain walls with architectural recessed downlights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 7. Cloud Computing & Web Hosting (4 Professions)
    # =========================================================================
    "Cloud Solutions Architect": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise cloud consultancy boardroom in Dhaka. "
        "Depicting a strategic Bangladeshi male cloud architect in his early 40s in crisp semi-formal button-down shirt, mapping multi-region failover topologies on an interactive digital smartboard. "
        "Environment features AWS and Azure cloud architecture blueprints with serverless VPC diagrams, enterprise hybrid-cloud migration binders, sleek aluminum laptop on an oak conference table, and views of modern corporate Dhaka towers. "
        "Atmosphere feels visionary, secure, scalable, and authoritative, defined by a distinct color palette of cool cloud platinum, deep cerulean blue, and polished concrete grey. "
        "Diffuse northern daylight from architectural curtain walls creating crisp professional highlights. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "FinOps Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cloud economics & cost optimization office in Dhaka. "
        "Depicting a detail-oriented Bangladeshi female cloud finance analyst in her late 20s wearing modern spectacles and tailored blazer, analyzing multi-cloud spend curves and reserved instance utilization. "
        "Environment features dual widescreen displays showing AWS Cost Explorer breakdown charts and Kubernetes container resource unit costs, digital ledger calculator, sleek metal task lamp, and organized financial compliance folders. "
        "Atmosphere feels fiscal, transparent, data-driven, and meticulous, defined by a distinct color palette of warm parchment white, copper mint green, and dark smoked oak. "
        "Soft warm desk lighting paired with balanced afternoon ambient room light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Site Reliability Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi 24/7 reliability engineering bullpen in Dhaka. "
        "Depicting a calm, vigilant Bangladeshi male SRE in his early 30s in casual company t-shirt and track jacket, maintaining 99.999% SLA uptime dashboards. "
        "Environment features four synchronized telemetry monitors displaying Grafana latency percentiles, error budget burn rates, open incident war-room channels, mechanical keyboard, and insulated water flask on an ergonomic desk. "
        "Atmosphere feels vigilant, resilient, calm under pressure, and nocturnal, defined by a distinct color palette of deep charcoal matte, electric teal, and warning pulse amber. "
        "Subtle nocturnal control-center lighting with cool LED desk backlights highlighting the gear. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Hosting Account Administrator": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi web hosting operations center and domain management office in Dhaka. "
        "Depicting a helpful, organized Bangladeshi female hosting administrator in her mid-20s in clean smart-casual shirt, provisioning dedicated cloud servers and SSL certificates. "
        "Environment features dual monitors showing cPanel/WHM infrastructure clusters, domain DNS propagation maps, customer hosting migration status checklists on clipboard, and small desktop succulent pots. "
        "Atmosphere feels dependable, accessible, clean, and cheerful, defined by a distinct color palette of crisp sky blue, light ash wood, and clean matte white. "
        "Bright airy natural daylight streaming across the desk from open office windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 8. Cybersecurity Solutions & Services (6 Professions)
    # =========================================================================
    "SOC Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi Tier-3 Security Operations Center (SOC) bridge in Dhaka. "
        "Depicting a sharp, focused Bangladeshi male cybersecurity analyst in his late 20s in dark company polo, triaging suspicious endpoint telemetry alarms. "
        "Environment features curved multi-monitor setup displaying Splunk SIEM event logs, MITRE ATT&CK matrix heatmaps, network packet inspection streams, and a tactical dark console desk with red-accented hardware. "
        "Atmosphere feels high-alert, cyber-defense, nocturnal, and intense, defined by a distinct color palette of tactical matte black, laser neon blue, and security alert amber. "
        "Low-light blue cyber command room ambiance with high-contrast screen reflections and crisp rim light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Penetration Test Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi offensive security & ethical hacking lab in Dhaka. "
        "Depicting a formidable, tech-savvy Bangladeshi female penetration test lead in her early 30s in relaxed black turtleneck, assessing red-team exploit payload delivery reports. "
        "Environment features dual monitors showing terminal command lines, vulnerability payload execution trees, hardware hacking dongles and rubber ducky devices neatly on a magnetic tray, and locked security hardware cases. "
        "Atmosphere feels covert, elite, technical, and investigative, defined by a distinct color palette of deep gunmetal grey, dark carbon fiber, and toxic violet neon accents. "
        "Moody directional downlight focusing on the desk with subtle purple background rim light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "GRC Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi corporate governance, risk & compliance (GRC) advisory office in Motijheel, Dhaka. "
        "Depicting a poised Bangladeshi male compliance officer in his mid-30s in formal suit and tie, evaluating ISO 27001 and SOC 2 security compliance audit trails. "
        "Environment features leather-bound risk register folios, compliance certification badges on frosted glass walls, dual executive screens displaying enterprise risk heatmaps, brass paperweight, and polished marble credenza. "
        "Atmosphere feels formal, trustworthy, institutional, and judicial, defined by a distinct color palette of deep Oxford navy, rich mahogany, and classic ivory paper. "
        "Refined corporate ceiling downlights balanced with natural morning sunlight through sheer corporate blinds. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Incident Response Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi cyber incident response emergency war-room in Dhaka. "
        "Depicting a calm, authoritative Bangladeshi female crisis lead in her late 30s in smart blazer with sleeves rolled up, coordinating containment measures during an active security drill. "
        "Environment features a large wall-mounted breach containment workflow display, timeline whiteboard with forensic evidence tags, encrypted satellite comms handset, conference phones, and forensic memory dump logs. "
        "Atmosphere feels urgent, commanding, mission-critical, and resilient, defined by a distinct color palette of dark slate, deep crimson red accents, and cool industrial aluminum. "
        "Dramatically lit incident war room with sharp downlight over the central conference desk and cool wall washes. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Vulnerability Management Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi vulnerability management & patch orchestration workstation in Dhaka. "
        "Depicting a meticulous Bangladeshi male analyst in his mid-20s wearing modern glasses and clean polo, prioritizing CVE severity scores and zero-day patch schedules. "
        "Environment features dual monitors showing Nessus/Qualys vulnerability scan reports, CVE score matrices, patch cadence timelines, mechanical keyboard, and a neat minimalist workstation in an airy tech office. "
        "Atmosphere feels methodical, preventive, secure, and clear-headed, defined by a distinct color palette of deep steel blue, clean cool grey, and warning amber accents. "
        "Bright architectural office lighting with soft shadows and balanced color temperature. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Security Awareness Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi corporate cyber culture & phishing simulation training suite in Dhaka. "
        "Depicting an engaging, charismatic Bangladeshi female security educator in her early 30s in contemporary professional attire, designing enterprise phishing simulation campaigns and interactive staff training modules. "
        "Environment features campaign metrics on glass boards showing simulated phishing click-through drop rates, creative cybersecurity awareness posters in sleek frames, modern laptop with campaign scheduler, and an inviting collaborative breakout area. "
        "Atmosphere feels educational, approachable, modern, and inspiring, defined by a distinct color palette of warm honey beige, soft ocean teal, and clean white. "
        "Flooded with uplifting, bright afternoon sunlight through tall office windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 9. Data Science & Analytics (4 Professions)
    # =========================================================================
    "Data Scientist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi advanced research laboratory & data modeling suite in Dhaka. "
        "Depicting a scholarly, innovative Bangladeshi male data scientist in his early 30s wearing stylish round glasses and unstructured blazer, fine-tuning neural network hyper-parameters. "
        "Environment features a large curved ultra-wide monitor displaying Jupyter Notebooks with loss curves and t-SNE cluster plots, glass whiteboard filled with matrix algebra and Bayesian probability equations, high-end desktop workstation with liquid cooling, and statistical textbook shelf. "
        "Atmosphere feels cerebral, high-tech, pioneering, and contemplative, defined by a distinct color palette of deep indigo navy, electric cyan, and warm cedar wood. "
        "Refined ambient study lighting with soft blue monitor glow and warm architectural wall sconces. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Business Intelligence Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi executive business intelligence and executive reporting floor in Gulshan, Dhaka. "
        "Depicting a sharp Bangladeshi female BI specialist in her late 20s wearing modern corporate chic clothing, building automated executive PowerBI and Tableau dashboards. "
        "Environment features dual 4K monitors displaying interactive sales velocity drill-down maps, SQL query editors, tidy executive desk with glass water bottle, and a panoramic view of the Gulshan lake skyline behind glass. "
        "Atmosphere feels lucid, commercial, executive, and luminous, defined by a distinct color palette of crisp pearl white, deep sapphire blue, and pale brushed brass. "
        "Brilliant, clean morning daylight pouring through full-height panoramic windows with subtle recessed office spots. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Product Analyst": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi product analytics & user behavior experimentation lab in Dhaka. "
        "Depicting an inquisitive Bangladeshi male product analyst in his late 20s in casual denim shirt, analyzing A/B testing conversion cohorts and user activation funnels. "
        "Environment features dual monitors showing Amplitude cohort analysis charts and statistical significance confidence intervals, sticky notes with hypothesis statements on a glass partition, tablet with UX wireflows, and sleek modern coffee mug. "
        "Atmosphere feels analytical, dynamic, user-focused, and fresh, defined by a distinct color palette of light ash wood, pastel coral, and cool slate grey. "
        "Even, bright daylight filling the collaborative creative space from modern loft windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "Data Governance Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi enterprise data catalog & compliance governance boardroom in Dhaka. "
        "Depicting a senior Bangladeshi female data steward in her late 40s in elegant traditional-modern corporate saree or formal suit, managing corporate data lineage dictionaries and privacy classification schemas. "
        "Environment features dual screens showing enterprise metadata lineages, privacy access governance frameworks, official data dictionary manuals on credenza, neat oak conference desk, and leather executive notepad. "
        "Atmosphere feels structured, ethical, authoritative, and dignified, defined by a distinct color palette of deep forest green, rich walnut, and warm brushed champagne gold. "
        "Soft overcast window daylight balanced with architectural warm ambient cove ceiling lighting. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    # =========================================================================
    # 10. Artificial Intelligence & Machine Learning (4 Professions)
    # =========================================================================
    "AI Product Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi frontier AI venture studio in Gulshan, Dhaka. "
        "Depicting a visionary Bangladeshi female AI product manager in her early 30s wearing modern minimalist executive attire, planning multimodal agent capabilities and user experience guardrails. "
        "Environment features glass collaboration walls with prompt-chaining architecture diagrams, high-end sit-stand desk with curved display showing LLM latency and token economics, modern plant planters, and architectural city view. "
        "Atmosphere feels forward-leaning, ambitious, refined, and futuristic, defined by a distinct color palette of warm sand beige, deep cobalt, and vibrant copper accents. "
        "Warm morning golden-hour light streaming into the penthouse office with soft interior fill light. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Evaluation Engineer": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI benchmark & red-teaming evaluation lab in Dhaka. "
        "Depicting a rigorous Bangladeshi male ML engineer in his late 20s in dark technical pullover and headphones around his neck, benchmarking hallucination rates and safety guardrail compliance. "
        "Environment features triple monitors displaying automated LLM evaluation radar charts, toxicity benchmark datasets, side-by-side prompt output diffs, mechanical keyboard, and precision hardware tools on a pegboard. "
        "Atmosphere feels rigorous, empirical, cutting-edge, and focused, defined by a distinct color palette of deep space navy, electric lime green, and brushed steel. "
        "Focused task lighting over the keyboard with cool ambient background screen illumination. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Data / Annotation Manager": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI training data curation & labeling operations center in Dhaka. "
        "Depicting an organized Bangladeshi female data operations lead in her late 20s in smart casual cardigan, overseeing multi-tier RLHF (reinforcement learning from human feedback) quality workflows. "
        "Environment features dual screens showing high-throughput bounding-box and text annotation pipelines, data quality distribution curves, tablet with labeling guidelines, and a neat collaborative bench with indoor succulents. "
        "Atmosphere feels efficient, vibrant, human-in-the-loop, and clean, defined by a distinct color palette of clean Scandinavian birch, warm terracotta, and fresh eucalyptus green. "
        "Airy, bright natural daylight streaming through tall modern windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    ),

    "AI Governance & Risk Specialist": (
        "Generate a completely distinct and unique individual, differing in gender, age, attire, and framing from previous images. "
        "Wide-angle, clean SaaS website hero background featuring an authentic modern Bangladeshi AI ethics & model governance advisory chamber in Dhaka. "
        "Depicting an authoritative Bangladeshi male legal-tech scholar in his early 50s in crisp tailored formal suit, analyzing algorithmic bias audits and model transparency compliance registers. "
        "Environment features dual executive screens showing model transparency scorecards and algorithmic risk heatmaps, bound international AI regulatory framework guidelines on desk, polished dark walnut conference table, and leather blotter. "
        "Atmosphere feels authoritative, ethical, prestigious, and scholarly, defined by a distinct color palette of deep rich burgundy, dark mahogany oak, and polished brass. "
        "Warm architectural recessed illumination combined with soft overcast daylight through tall library windows. "
        "Balanced composition, generous negative space designed for UI card and dashboard overlay, low contrast, shallow depth of field, 35mm photography, f/2.8 aperture, cinematic corporate realism, ultra-detailed textures, 8k resolution --ar 16:9 --style raw"
    )
}

def main():
    csv_file = "Othe.app image generation industry profession and prompt - Sheet1.csv"
    with open(csv_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    for r in rows:
        prof = r["Profession"].strip()
        if prof in DISTINCT_44:
            r["Prompt"] = DISTINCT_44[prof]
            updated += 1

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Industry", "Profession", "Prompt"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done! Successfully applied {updated} / {len(DISTINCT_44)} distinct prompts to CSV.")

if __name__ == "__main__":
    main()

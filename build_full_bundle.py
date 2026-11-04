import re
import os

with open("main_orig.js", "r") as f:
    js = f.read()

print("Original length:", len(js))

# ==============================================================================
# A. Stage: ASIAN PAINTS HQ IT FLOOR (buildHeadOffice + apFloorTex)
# ==============================================================================
print("A. Adding Head Office stage...")

# 1. Add apFloorTex helper before var Ft=[
floor_tex_helper = """function apFloorTex(){
  let c = document.createElement("canvas");
  c.width = 1024; c.height = 1024;
  let ctx = c.getContext("2d");
  ctx.fillStyle = "#1e1e24";
  ctx.fillRect(0, 0, 1024, 1024);
  ctx.strokeStyle = "rgba(255,255,255,0.04)";
  ctx.lineWidth = 2;
  for (let x = 0; x <= 1024; x += 128) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke();
  }
  for (let y = 0; y <= 1024; y += 128) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke();
  }
  for (let i = 0; i < 16; i++) {
    let rx = Math.floor(Math.random() * 8) * 128;
    let ry = Math.floor(Math.random() * 8) * 128;
    ctx.fillStyle = i % 2 === 0 ? "rgba(216, 35, 42, 0.12)" : "rgba(247, 181, 0, 0.08)";
    ctx.fillRect(rx + 2, ry + 2, 124, 124);
  }
  let tex = new _e(c);
  tex.colorSpace = oe;
  tex.anisotropy = 4;
  tex.wrapS = 1000;
  tex.wrapT = 1000;
  tex.repeat.set(4, 2);
  return tex;
}
"""

idx_ft_init = js.find("var Ft=[")
assert idx_ft_init != -1, "var Ft=[ not found"
js = js[:idx_ft_init] + floor_tex_helper + js[idx_ft_init:]

# 2. Add headoffice in themeGroups and floorTextures
old_tg = "e(this,`themeGroups`,{sansad:new c,jantar:new c,road:new c})"
new_tg = "e(this,`themeGroups`,{sansad:new c,jantar:new c,road:new c,headoffice:new c})"
assert old_tg in js, "themeGroups declaration not found"
js = js.replace(old_tg, new_tg)

old_tgr = "this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road)"
new_tgr = "this.group.add(this.themeGroups.sansad,this.themeGroups.jantar,this.themeGroups.road,this.themeGroups.headoffice)"
assert old_tgr in js, "this.group.add themeGroups not found"
js = js.replace(old_tgr, new_tgr)

old_ft = "this.floorTextures={sansad:At(),jantar:jt(),road:_t(Et)}"
new_ft = "this.floorTextures={sansad:At(),jantar:jt(),road:_t(Et),headoffice:apFloorTex()}"
assert old_ft in js, "floorTextures not found"
js = js.replace(old_ft, new_ft)

old_ct = "Ct(this.themeGroups.road),"
new_ct = "Ct(this.themeGroups.road),this.buildHeadOffice(this.themeGroups.headoffice),"
assert old_ct in js, "Ct call not found"
js = js.replace(old_ct, new_ct)

# 3. Add Tt stage metadata for headoffice
js = js.replace(
    "road:{skyTop:2239805,skyMid:6190740,skyBottom:12895690,fog:12895690,fogNear:30,fogFar:80,ground:6711400,platformSide:5329233,floorRoughness:.95,sunColor:16773340,sunPos:[5,7,12],hemiSky:15066850,hemiGround:6711400,sunDisc:[-8,12,-40],sunDiscColor:16773340,exposure:1.15}",
    "road:{skyTop:2239805,skyMid:6190740,skyBottom:12895690,fog:12895690,fogNear:30,fogFar:80,ground:6711400,platformSide:5329233,floorRoughness:.95,sunColor:16773340,sunPos:[5,7,12],hemiSky:15066850,hemiGround:6711400,sunDisc:[-8,12,-40],sunDiscColor:16773340,exposure:1.15},headoffice:{skyTop:1315860,skyMid:2105376,skyBottom:3289650,fog:2631720,fogNear:25,fogFar:75,ground:1710618,platformSide:2631720,floorRoughness:.35,sunColor:16777215,sunPos:[0,10,-5],hemiSky:14474460,hemiGround:3289650,sunDisc:[0,15,-35],sunDiscColor:16777215,exposure:1.05}"
)

# 4. Add buildHeadOffice implementation to Lt
head_office_code = """buildHeadOffice(hq){
  let wallMat = new x({color: 0x22222a, roughness: 0.8});
  let backWall = new p(new C(48, 12, 1), wallMat);
  backWall.position.set(0, 5.7, -14);
  hq.add(backWall);

  let brandRedMat = new x({color: 0xd8232a, roughness: 0.3, metalness: 0.2});
  let accentStrip = new p(new C(48, 0.45, 1.05), brandRedMat);
  accentStrip.position.set(0, 10.5, -13.9);
  hq.add(accentStrip);

  let brandYellowMat = new x({color: 0xf7b500, roughness: 0.3});
  let yellowStrip = new p(new C(48, 0.15, 1.05), brandYellowMat);
  yellowStrip.position.set(0, 10.1, -13.9);
  hq.add(yellowStrip);

  let deskMat = new x({color: 0xe0e0e0, roughness: 0.3, metalness: 0.1});
  let deskLegMat = new x({color: 0x333333, roughness: 0.5, metalness: 0.8});
  let glassMat = new g({color: 0x88ccff, transparent: true, opacity: 0.35});
  let partitionFrameMat = new x({color: 0x222222, roughness: 0.4});

  for (let side of [-1, 1]) {
    let cabin = new c;
    cabin.position.set(side * 14.5, 0, -10);
    let frontGlass = new p(new C(7.5, 4.2, 0.08), glassMat);
    frontGlass.position.set(0, 2.1, 0);
    cabin.add(frontGlass);
    let topFrame = new p(new C(7.6, 0.12, 0.12), partitionFrameMat);
    topFrame.position.set(0, 4.2, 0);
    cabin.add(topFrame);
    let cabinDesk = new p(new C(3.2, 0.1, 1.4), new x({color: 0x3d2314, roughness: 0.2}));
    cabinDesk.position.set(0, 0.9, -2.2);
    cabin.add(cabinDesk);
    let cLight = new ne(side > 0 ? 0xfffaed : 0xebf4ff, 2.8, 8, 1.5);
    cLight.position.set(0, 3.8, -2);
    cLight.userData.keepLight = true;
    cabin.add(cLight);
    hq.add(cabin);
  }

  let monitorMat = new x({color: 0x111111, roughness: 0.2, metalness: 0.9});
  let codeScreenMat = new g({color: 0x00ff88});
  let erpScreenMat = new g({color: 0x00b4d8});

  for (let dx of [-9, -4.5, 0, 4.5, 9]) {
    let deskPod = new c;
    deskPod.position.set(dx, 0, -6.5);
    let top = new p(new C(3.4, 0.08, 1.4), deskMat);
    top.position.set(0, 0.85, 0);
    deskPod.add(top);
    for (let lx of [-1.55, 1.55]) {
      let leg = new p(new C(0.08, 0.85, 1.3), deskLegMat);
      leg.position.set(lx, 0.425, 0);
      deskPod.add(leg);
    }
    let divider = new p(new C(3.4, 0.5, 0.06), new x({color: 0xd8232a, roughness: 0.8}));
    divider.position.set(0, 1.15, -0.65);
    deskPod.add(divider);

    for (let mx of [-0.65, 0.65]) {
      let stand = new p(new E(0.03, 0.03, 0.35, 8), deskLegMat);
      stand.position.set(mx, 1.05, -0.3);
      deskPod.add(stand);
      let screen = new p(new C(0.85, 0.5, 0.04), monitorMat);
      screen.position.set(mx, 1.25, -0.3);
      screen.rotation.y = mx < 0 ? 0.08 : -0.08;
      deskPod.add(screen);
      let display = new p(new C(0.8, 0.45, 0.01), mx < 0 ? codeScreenMat : erpScreenMat);
      display.position.set(mx, 1.25, -0.28);
      display.rotation.y = screen.rotation.y;
      deskPod.add(display);
    }

    let chairMat = new x({color: 0x222222, roughness: 0.6});
    let chairSeat = new p(new C(0.55, 0.08, 0.5), chairMat);
    chairSeat.position.set(0, 0.55, 0.45);
    deskPod.add(chairSeat);
    let chairBack = new p(new C(0.5, 0.6, 0.06), chairMat);
    chairBack.position.set(0, 0.88, 0.68);
    deskPod.add(chairBack);

    hq.add(deskPod);
  }

  let rackMat = new x({color: 0x151515, roughness: 0.3, metalness: 0.7});
  let ledGreen = new g({color: 0x00ff00});
  let ledBlue = new g({color: 0x0088ff});
  for (let rx of [-18, 18]) {
    let rackGroup = new c;
    rackGroup.position.set(rx, 0, -8);
    for (let rz of [-2, 0, 2]) {
      let rack = new p(new C(1.2, 4.5, 1.2), rackMat);
      rack.position.set(0, 2.25, rz);
      rackGroup.add(rack);
      for (let ly = 0.6; ly <= 4.0; ly += 0.35) {
        let led = new p(new C(0.04, 0.03, 0.02), Math.random() > 0.5 ? ledGreen : ledBlue);
        led.position.set(rx < 0 ? 0.61 : -0.61, ly, rz + (Math.random() - 0.5) * 0.8);
        rackGroup.add(led);
      }
    }
    let rackLight = new ne(0x0088ff, 2.2, 6, 1.4);
    rackLight.position.set(rx < 0 ? 1 : -1, 2.5, 0);
    rackLight.userData.keepLight = true;
    rackGroup.add(rackLight);
    hq.add(rackGroup);
  }

  for (let tx of [-8, 0, 8]) {
    for (let tz of [-3, -7, -11]) {
      let lightFixt = new p(new C(2.8, 0.1, 1.2), new g({color: 0xffffff}));
      lightFixt.position.set(tx, 9.5, tz);
      hq.add(lightFixt);
    }
  }
}
"""

idx_sansad = js.find("buildSansad(e){")
assert idx_sansad != -1, "buildSansad not found"
js = js[:idx_sansad] + head_office_code + js[idx_sansad:]


# ==============================================================================
# B. Character Roster: DIBY (Abdul) and MADHUMAN (Modi)
# ==============================================================================
print("B. Updating character roster & descriptions...")

# 1. Update A.modi
old_modi_entry = "modi:{id:`modi`,name:`MITRAMAN`,fullName:`MitraMan`,party:`Team Vaada`,accent:`#ff9933`,look:{skin:12748377,skinShade:10907206,hair:15921386,hairStyle:`receding`,beard:16052972,beardStyle:`full-white`,brows:15263456,topStyle:`kurta-jacket`,top:15985362,jacket:15764004,pants:16184038,shoes:3875862,glasses:!0,shoulders:1.05,belly:1.25,scale:1},walkFwd:2.1,walkBack:1.6,jumpV:7.6,jumpVx:2.4,damageMul:1.08,moveNames:{special1:`DEMONETIZATION PALM!`,special2:`SURPRISE STRIKE!`,finisher:`LAMBA BHASHAN COMBO!`,sweep:`GST SWEEP!`,uppercut:`VIKAS UPPERCUT!`,grab:`HUGPLOMACY!`,roundhouse:`SUNEHRE DIN ROUNDHOUSE!`},superName:`MITRA CHAKRA`,superDesc:`Rises into the sky as a spinning chakra grows from a spark, then hurls it for 30% damage.`,introLine:`Mitron!`,winLine:`Is baar, jeet hamari!`"
new_modi_entry = "modi:{id:`modi`,name:`MADHUMAN`,fullName:`Madhuman`,party:`Asian Paints · AGM (Automation & AI)`,accent:`#76b900`,look:{skin:12748377,skinShade:10907206,hair:15921386,hairStyle:`receding`,beard:16052972,beardStyle:`full-white`,brows:15263456,topStyle:`kurta-jacket`,top:15985362,jacket:15764004,pants:16184038,shoes:3875862,glasses:!0,shoulders:1.05,belly:1.25,scale:1},walkFwd:2.1,walkBack:1.6,jumpV:7.6,jumpVx:2.4,damageMul:1.08,moveNames:{special1:`VIBE CODE PALM!`,special2:`GPU SURGE STRIKE!`,finisher:`FULL AUTOMATION COMBO!`,sweep:`BACKLOG SWEEP!`,uppercut:`TENSOR UPPERCUT!`,grab:`STANDUP MEETING GRAB!`,roundhouse:`100X DEV ROUNDHOUSE!`},superName:`AI GPU CLUSTER`,superDesc:`Summons an orbital storm of overclocked AI GPUs and neural accelerators, screaming 'Vibe code krta h?' & 'Sab automate kr dunga' for 38% damage!`,introLine:`Sab automate kr dunga! Vibe code dekha hai?`,winLine:`Done in 1 prompt! 100% automated!`"
assert old_modi_entry in js, "old_modi_entry not found"
js = js.replace(old_modi_entry, new_modi_entry)

# 2. Add abdul / diby entry to A
diby_entry = """abdul:{id:`abdul`,name:`DIBY`,fullName:`Diby`,party:`Asian Paints · Network Specialist`,accent:`#d8232a`,look:{skin:13802352,skinShade:11894874,hair:3090983,hairStyle:`side-part`,beard:3090983,beardStyle:`none`,brows:3090983,topStyle:`shirt`,top:14164778,jacket:14164778,pants:13156000,shoes:2236962,glasses:!1,shoulders:1,belly:.95,scale:1},walkFwd:2.3,walkBack:1.8,jumpV:8,jumpVx:2.6,damageMul:1.15,moveNames:{special1:`PACKET STORM!`,special2:`FIREWALL KICK!`,finisher:`SWITCH REBOOT COMBO!`,sweep:`LAN CABLE SWEEP!`,uppercut:`BANDWIDTH UPPERCUT!`,grab:`MAC TABLE GRAB!`,roundhouse:`ROUTER RESTART ROUNDHOUSE!`},superName:`NETWORK FREEZE`,superDesc:`Pulls out a company ThinkPad, blocks network access, freezes opponent with "Jaa SR raise krke aa" and unleashes a barrage of strikes for 38% damage!`,introLine:`Network freeze ho jayega, warning de raha hu!`,winLine:`SR closed: Rejected! Connection terminated!`},"""

js = js.replace("A={modi:", f"A={{{diby_entry}modi:")

# 3. Model URLs for abdul & Portrait in Hl
js = js.replace("Oo={modi:", "Oo={abdul:`/models/abdul.glb?v=abdul_v3`,modi:")
js = js.replace("ko={modi:", "ko={abdul:`/models/abdul.glb?v=abdul_v3`,modi:")

old_hl = "Hl={modi:`${Bl}faces/modi.png${Vl}`"
new_hl = "Hl={abdul:`${Bl}faces/abdul.png${Vl}`,modi:`${Bl}faces/modi.png${Vl}`"
assert old_hl in js, "Hl not found"
js = js.replace(old_hl, new_hl)

# 4. Newsdesk chatter in Oi
old_oi = "Oi={modi:{hype:`MITRA CHAKRA! Goosebumps, mitron!`,spin:`Bro brought a pizza cutter to a fight 💀`,ticker:`Seismologists alarmed`}"
new_oi = """Oi={abdul:{hype:`DIBY ACTIVATES NETWORK FREEZE! Access Revoked!`,spin:`Bro cut the opponent's WiFi and beat him up during downtime 💀`,ticker:`Network Specialist Diby shuts down all ports; 'Jaa SR raise krke aa' trends #1`},modi:{hype:`AI GPU CLUSTER! Sab automate kr dunga!`,spin:`Bro vibe-coded the entire supermove on 8x H100 GPUs 💀`,ticker:`AGM Madhuman automates opponent out of the job; HR notified`}"""
assert old_oi in js, "old_oi not found"
js = js.replace(old_oi, new_oi)


# ==============================================================================
# C. Super Move 1: DIBY'S NETWORK FREEZE (AbdulSuper)
# ==============================================================================
print("C. Adding AbdulSuper (Network Freeze)...")

network_freeze_code = """var AbdulSuper = class extends ka {
  constructor(ctx) {
    super(ctx);
    e(this, "root", new c);
    e(this, "laptop", void 0);
    e(this, "screenGlow", void 0);
    e(this, "wifiRings", []);
    e(this, "freezeBarrier", void 0);
    e(this, "beatCount", 0);
    e(this, "finalHitDone", false);

    ctx.scene.add(this.root);
    let caster = ctx.caster;
    let target = ctx.target;
    let facing = caster.facing;

    // --- 3D Corporate Laptop (ThinkPad style) ---
    this.laptop = new c;
    let baseMesh = new p(new C(0.42, 0.025, 0.3), new x({ color: 1776411, roughness: 0.4, metalness: 0.6 }));
    this.laptop.add(baseMesh);
    let kbMesh = new p(new C(0.36, 0.005, 0.22), new x({ color: 2631720, roughness: 0.7 }));
    kbMesh.position.set(0, 0.015, 0.02);
    this.laptop.add(kbMesh);
    let screenPivot = new c;
    screenPivot.position.set(0, 0.015, -0.14);
    screenPivot.rotation.x = -Math.PI * 0.58;
    let lidMesh = new p(new C(0.42, 0.3, 0.02), new x({ color: 1776411, roughness: 0.4 }));
    lidMesh.position.set(0, 0.15, 0);
    screenPivot.add(lidMesh);
    let screenFace = new p(new C(0.38, 0.26, 0.005), new g({ color: 16724530 }));
    screenFace.position.set(0, 0.15, 0.012);
    screenPivot.add(screenFace);
    this.laptop.add(screenPivot);

    this.laptop.position.set(caster.x + facing * 0.45, 1.15, 0);
    this.root.add(this.laptop);

    this.screenGlow = new ne(16724530, 2.8, 4, 1.2);
    this.screenGlow.position.set(caster.x + facing * 0.5, 1.3, 0);
    this.root.add(this.screenGlow);

    for (let i = 0; i < 5; i++) {
      let ringMat = new g({ color: 16724530, transparent: true, opacity: 0.8 });
      let ring = new p(new E(0.5 + i * 0.25, 0.55 + i * 0.25, 0.04, 24), ringMat);
      ring.rotation.x = Math.PI / 2;
      ring.position.set(target.x, 0.2 + i * 0.35, 0);
      ring.scale.setScalar(0.001);
      this.root.add(ring);
      this.wifiRings.push(ring);
    }

    let barrierMat = new g({ color: 5635327, transparent: true, opacity: 0.35 });
    this.freezeBarrier = new p(new E(0.85, 0.85, 2.2, 8), barrierMat);
    this.freezeBarrier.position.set(target.x, 1.1, 0);
    this.freezeBarrier.scale.setScalar(0.001);
    this.root.add(this.freezeBarrier);

    ctx.audio.uiTap?.();
    ctx.audio.whoosh?.();
  }

  step(dt) {
    let ctx = this.d;
    this.advance(dt, 0);
    let t = this.t;
    let caster = ctx.caster;
    let target = ctx.target;
    let facing = caster.facing;
    let cue = (time) => t >= time && t - dt < time;

    // --- PHASE 1: [0.0s - 1.0s] The Laptop & Access Revocation ---
    if (t < 1.0) {
      this.casterPose = M(R(t, "rahul"), {
        spineF: 0.15,
        rShF: 1.1, rShO: 0.1, rEl: 1.8, rHand: 1,
        lShF: 1.1, lShO: 0.1, lEl: 1.8, lHand: 1,
        headF: 0.2
      });

      this.laptop.position.y = 1.15 + Math.sin(t * 18.0) * 0.015;

      if (cue(0.1)) {
        ctx.audio.uiTap?.();
      }
      if (cue(0.35)) {
        ctx.audio.uiConfirm?.();
        ctx.popup("NETWORK ACCESS BLOCKED!", this.v1.set(caster.x + facing * 0.5, 2.1, 0), "#ff2233");
      }
      if (cue(0.6)) {
        ctx.speech("caster", "JAA SR RAISE KRKE AA!");
        ctx.popup("JAA SR RAISE KRKE AA!", this.v1.set(target.x, 2.3, 0), "#ffe3a0");
        ctx.audio.thunder?.();
        ctx.flash("rgba(255, 34, 51, 0.4)", 150);
      }
    }

    // --- PHASE 2: [1.0s - 2.8s] Network Freeze & The Beatdown ---
    if (t >= 1.0 && t < 2.8) {
      if (this.laptop) {
        this.laptop.visible = false;
      }
      if (this.screenGlow) {
        this.screenGlow.visible = false;
      }

      this.freezeBarrier.scale.setScalar(Math.min(1.0, (t - 1.0) * 4.0));
      this.targetPose = M(R(t, "modi"), {
        spineF: -0.2, headF: 0.3,
        rShF: 0.3, lShF: 0.3,
        lThF: 0.1, rThF: 0.1
      });

      let targetStandX = target.x - facing * 0.75;
      caster.x += (targetStandX - caster.x) * Math.min(1.0, dt * 10.0);

      let strikeCycle = ((t - 1.0) * 4.5) % 4.0;
      if (strikeCycle < 1.0) {
        this.casterPose = M(R(t, "rahul"), {
          spineT: -0.35, rShF: 0.6, rEl: 2.1,
          lShF: 1.6, lShO: -0.1, lEl: 0.05, rootZ: 0.1
        });
      } else if (strikeCycle < 2.0) {
        this.casterPose = M(R(t, "rahul"), {
          spineT: 0.4, lShF: 0.7, lEl: 2.1,
          rShF: 1.65, rShO: -0.15, rEl: 0.05, rootZ: 0.15
        });
      } else if (strikeCycle < 3.0) {
        this.casterPose = M(R(t, "rahul"), {
          spineF: -0.2, rThF: 1.5, rKn: 0.15, rAnk: 0.2,
          lShF: 0.5, rShF: 1.1, rEl: 1.5
        });
      } else {
        this.casterPose = M(R(t, "rahul"), {
          spineF: -0.25, spineT: -0.3,
          lShF: 2.7, lShO: -0.1, lEl: 0.45, rShF: 0.8, rEl: 2.0
        });
      }

      let hitMoments = [1.15, 1.45, 1.75, 2.05, 2.35];
      for (let hm of hitMoments) {
        if (cue(hm)) {
          ctx.audio.thud?.();
          ctx.cam.shake(0.2, 0.25);
          ctx.fx.particles.emit(this.v1.set(target.x, target.y + 1.2, 0), {
            count: 14,
            speed: 3.2,
            color: 5635327,
            life: 0.5,
            size: 0.2
          });
          target.hp = Math.max(1, target.hp - 2);
        }
      }
    }

    // --- PHASE 3: [2.8s - 3.8s] Final Blow ---
    if (t >= 2.8) {
      if (cue(2.85)) {
        ctx.speech("caster", "TICKET CLOSED! NO INTERNET FOR YOU!");
        ctx.popup("SR RESOLVED: REJECTED!", this.v1.set(target.x, 2.2, 0), "#d8232a");
      }

      if (t < 3.1) {
        this.casterPose = M(R(t, "rahul"), {
          spineF: -0.3, spineT: 0.4,
          rShF: 2.8, rShO: 0.3, rEl: 0.5, rootY: -0.1
        });
      } else {
        this.casterPose = M(R(t, "rahul"), {
          spineF: 0.5, spineT: -0.4,
          rShF: 1.6, rShO: -0.2, rEl: 0.05, rootZ: 0.2
        });
      }

      if (t >= 3.1 && !this.finalHitDone) {
        this.finalHitDone = true;
        ctx.audio.boom?.();
        ctx.audio.thunder?.();
        ctx.cam.shake(0.5, 0.7);
        ctx.flash("rgba(216, 35, 42, 0.6)", 220);

        if (this.freezeBarrier) {
          this.freezeBarrier.visible = false;
        }

        for (let col of [16724530, 5635327, 16777215]) {
          ctx.fx.particles.emit(this.v1.set(target.x, target.y + 1.2, 0), {
            count: 35,
            speed: 5.5,
            color: col,
            life: 0.9,
            size: 0.32,
            gravity: 7,
            drag: 1.1
          });
        }

        ctx.popup("DOWNTIME MAXIMUM!", this.v1.set(target.x, target.y + 2.0, 0), "#ff2233");
        this.landSuperHit(target.hp, facing, 4.8, 6.5, 0.32);
      }
    }

    this.settleTarget(dt);

    if (this.finalHitDone) {
      this.targetPose = null;
      target.update(Ur(), caster.x);
    }

    // Dynamic Camera Tracking
    if (t < 1.0) {
      this.v2.set(caster.x + facing * 1.5, 1.45, 2.8);
      this.v3.set(caster.x + facing * 0.35, 1.25, 0);
      ctx.cam.set(this.v2, this.v3, t < 0.1 ? 12 : 3.5, 38);
    } else if (t < 2.8) {
      let midX = (caster.x + target.x) / 2;
      this.v2.set(midX - facing * 0.4, 1.6, 4.2);
      this.v3.set(midX, 1.2, 0);
      ctx.cam.set(this.v2, this.v3, 4.0, 42);
    } else {
      let midX = (caster.x + target.x) / 2;
      this.v2.set(midX + facing * 0.5, 1.8, 5.8);
      this.v3.set(target.x, 1.1, 0);
      ctx.cam.set(this.v2, this.v3, 3.0, 45);
    }

    if (t >= 4.0) {
      caster.y = 0;
      if (target.hp > 0 && target.state === "frozen") {
        target.forceState("idle");
      }
      this.done = true;
    }
  }

  dispose() {
    this.root.removeFromParent();
    if (this.laptop) {
      this.laptop.traverse(m => {
        m.geometry?.dispose();
        m.material?.dispose();
      });
    }
    for (let r of this.wifiRings) {
      r.geometry?.dispose();
      r.material?.dispose();
    }
    if (this.freezeBarrier) {
      this.freezeBarrier.geometry?.dispose();
      this.freezeBarrier.material?.dispose();
    }
    if (this.screenGlow) {
      this.screenGlow.dispose?.();
    }
  }
};
"""

idx_ka = js.find("var Oa=new T(0,1,0),ka=class{")
idx_ka_end = js.find("};", idx_ka) + 2
assert idx_ka != -1, "ka class not found"
js = js[:idx_ka_end] + "\n" + network_freeze_code + "\n" + js[idx_ka_end:]

# Super move dispatch in Ws
js = js.replace("case`modi`:return new ja(e);", "case`abdul`:return new AbdulSuper(e);case`modi`:return new ja(e);")


# ==============================================================================
# D. Super Move 2: MADHUMAN'S AI GPU CLUSTER (Tech Chakra + Dialogue)
# ==============================================================================
print("D. Adding Tech GPUs to Chakra (Aa) and Madhuman dialogue (ja)...")

# 1. Update Aa() with 6 detailed 3D GPUs orbiting around spinner
tech_chakra_aa = """function Aa(){
  let e = new c, t = new c;
  e.add(t);

  // Holographic Quantum & Neural Accelerator Rings
  let n = new x({ color: 0x00ff88, emissive: 0x00bb55, emissiveIntensity: 0.9, metalness: 0.8, roughness: 0.2, side: 2 });
  let r = new x({ color: 0x00e5ff, emissive: 0x0099ff, emissiveIntensity: 1.3, metalness: 0.5, roughness: 0.2, side: 2 });
  let i = (geo, mat, px=0, py=0, rz=0) => {
    let o = new p(geo, mat);
    o.position.set(px, py, 0);
    o.rotation.z = rz;
    t.add(o);
    return o;
  };

  i(new w(1, 0.06, 10, 64), n);
  i(new w(0.82, 0.03, 8, 64), r);
  i(new w(0.45, 0.04, 8, 48), n);
  i(new Fe(0.24, 32), r);

  // 3D GPU Generator (NVIDIA RTX / AI Tensor Accelerator style)
  let makeGPU = () => {
    let gpu = new c;
    // Dark PCB Backplate
    let pcb = new p(new C(0.48, 0.22, 0.025), new x({ color: 0x152515, roughness: 0.4, metalness: 0.5 }));
    gpu.add(pcb);
    // Aluminum Heat sink
    let sink = new p(new C(0.44, 0.18, 0.04), new x({ color: 0x8899aa, roughness: 0.3, metalness: 0.8 }));
    sink.position.z = 0.035;
    gpu.add(sink);
    // Twin Cooling Fans
    for (let fx of [-0.12, 0.12]) {
      let fanRing = new p(new w(0.065, 0.012, 6, 16), new x({ color: 0x111111, roughness: 0.8 }));
      fanRing.position.set(fx, 0, 0.06);
      gpu.add(fanRing);
      let fanHub = new p(new E(0.025, 0.025, 0.015, 10), new x({ color: 0x444444, metalness: 0.8 }));
      fanHub.rotation.x = Math.PI / 2;
      fanHub.position.set(fx, 0, 0.065);
      gpu.add(fanHub);
    }
    // Glowing Tech Green LED strip
    let rtxLed = new p(new C(0.28, 0.03, 0.01), new g({ color: 0x76b900 }));
    rtxLed.position.set(0, 0.09, 0.055);
    gpu.add(rtxLed);
    // Gold PCIe pins
    let pcie = new p(new C(0.26, 0.03, 0.008), new x({ color: 0xffcc00, metalness: 0.9, roughness: 0.2 }));
    pcie.position.set(-0.04, -0.12, 0);
    gpu.add(pcie);
    return gpu;
  };

  // Attach 6 GPUs in orbital array around chakra perimeter
  for (let gIdx = 0; gIdx < 6; gIdx++) {
    let ang = gIdx / 6 * Math.PI * 2;
    let gpuObj = makeGPU();
    gpuObj.position.set(Math.cos(ang) * 1.18, Math.sin(ang) * 1.18, 0);
    gpuObj.rotation.z = ang + Math.PI / 2;
    gpuObj.scale.setScalar(0.95);
    t.add(gpuObj);
  }

  // Connecting Circuit Data Traces
  for (let e = 0; e < 12; e++) {
    let ang = e / 12 * Math.PI * 2;
    i(new C(0.025, 0.5, 0.02), n, Math.cos(ang) * 0.65, Math.sin(ang) * 0.65, ang - Math.PI / 2);
  }

  let blurMesh = new p(new m(0.25, 1.45, 64), new g({ color: 0x00ff88, transparent: true, opacity: 0, blending: 2, depthWrite: false, side: 2 }));
  e.add(blurMesh);
  let s = nt(0x00ff88, 3.6, 0.45);
  e.add(s);
  let l = nt(0x00e5ff, 1.4, 0.6);
  e.add(l);
  let u = new ne(0x00ff88, 0, 10, 2);
  e.add(u);

  return { root: e, spinner: t, light: u, glow: s, halo: l, blur: blurMesh };
}
"""

idx_aa = js.find("function Aa(){")
idx_aa_end = js.find("var ja=class", idx_aa)
assert idx_aa != -1, "Aa function not found"
js = js[:idx_aa] + tech_chakra_aa + js[idx_aa_end:]

# 2. Add Madhuman's Dialogue & Popups to ja.step()
idx_ja = js.find("var ja=class")
old_ja_step_head = "this.advance(e,i);let a=this.t,o=n.caster,s=o.facing;"
idx_advance = js.find(old_ja_step_head, idx_ja)
assert idx_advance != -1, "advance line in ja not found"

madhuman_cues = """this.advance(e,i);let a=this.t,o=n.caster,s=o.facing;
    let cueJa = (time) => a >= time && a - e < time;
    if (cueJa(0.35)) {
      n.speech(`caster`, `VIBE CODE KRTA H ?`);
      n.popup(`VIBE CODE KRTA H ?`, this.v1.set(o.x + s * 0.4, o.y + 2.5, 0), `#76b900`);
      n.audio.uiTap?.();
    }
    if (cueJa(3.8)) {
      n.popup(`AI GPU CLUSTER OVERCLOCKING...`, this.v1.set(o.x, o.y + 2.8, 0), `#00e5ff`);
    }
    if (cueJa(this.WIND)) {
      n.speech(`caster`, `SAB AUTOMATE KR DUNGA!`);
      n.popup(`SAB AUTOMATE KR DUNGA!`, this.v1.set(o.x + s * 0.5, o.y + 2.6, 0), `#ffea00`);
      n.audio.thunder?.();
    }
"""

js = js[:idx_advance] + madhuman_cues + js[idx_advance + len(old_ja_step_head):]

# On impact in ja:
old_ja_impact = "impactDone=!0,this.impactPoint.copy(l.root.position),this.landSuperHit(n.target.hp,s,4.6,8.5)"
new_ja_impact = "impactDone=!0,n.speech(`caster`,`DONE IN 1 PROMPT! 100% AUTOMATED!`),n.popup(`FULL AUTOMATION OVERLOAD!`,this.v1.set(n.target.x,2.4,0),`#76b900`),this.impactPoint.copy(l.root.position),this.landSuperHit(n.target.hp,s,4.6,8.5)"
assert old_ja_impact in js, "old_ja_impact not found"
js = js.replace(old_ja_impact, new_ja_impact)


# ==============================================================================
# E. Frustrated Employees Crowd Placards (Ft)
# ==============================================================================
print("E. Replacing crowd placards with frustrated employee demands...")

idx_ft = js.find("var Ft=[")
idx_ft_end = js.find("Lt=class{", idx_ft)
assert idx_ft != -1 and idx_ft_end != -1, "Ft array bounds not found"

office_placards = """var Ft=[
  {pool:`neutral`,text:`WFH DEDO!`,bg:`#d8232a`,fg:`#ffffff`},
  {pool:`neutral`,text:`LEAVE DE DO!`,bg:`#ffd23f`,fg:`#1a237e`},
  {pool:`neutral`,text:`HIKE KAB?!`,bg:`#ff9933`,fg:`#ffffff`},
  {pool:`neutral`,text:`TIMESHEET!`,bg:`#22b35e`,fg:`#ffffff`},
  {pool:`neutral`,text:`RATING 3 KYUN?`,bg:`#ffffff`,fg:`#c0392b`},
  {pool:`neutral`,text:`CHAI BREAK!`,bg:`#ffd700`,fg:`#1a1000`},
  {pool:`neutral`,text:`NO WEEKENDS!`,bg:`#1f6fe0`,fg:`#ffffff`},
  {pool:`neutral`,text:`LOG HOURS!`,bg:`#e06a00`,fg:`#ffffff`},
  {pool:`modi`,text:`VIBE CODING`,bg:`#76b900`,fg:`#ffffff`},
  {pool:`modi`,text:`SAB AUTOMATE!`,bg:`#00e5ff`,fg:`#000000`},
  {pool:`modi`,text:`AI FIRST!`,bg:`#000000`,fg:`#76b900`},
  {pool:`modi`,text:`GPU OVERCLOCK`,bg:`#76b900`,fg:`#000000`},
  {pool:`abdul`,text:`NET DOWN!`,bg:`#d8232a`,fg:`#ffffff`},
  {pool:`abdul`,text:`RAISE SR!`,bg:`#ffffff`,fg:`#d8232a`},
  {pool:`abdul`,text:`VPN CRASHED`,bg:`#00b4d8`,fg:`#ffffff`},
  {pool:`abdul`,text:`SWITCH REBOOT`,bg:`#d8232a`,fg:`#ffffff`},
  {pool:`rahul`,text:`RESIGNATION!`,bg:`#ffffff`,fg:`#1f6fe0`},
  {pool:`rahul`,text:`PIP NOTICE`,bg:`#1f6fe0`,fg:`#ffffff`},
  {pool:`trump`,text:`OFFSHORE US`,bg:`#c8102e`,fg:`#ffffff`},
  {pool:`trump`,text:`LAYOFF KING`,bg:`#ffffff`,fg:`#c8102e`},
  {pool:`yogi`,text:`ESCALATION!`,bg:`#f05a00`,fg:`#ffffff`},
  {pool:`yogi`,text:`INCIDENT P1!`,bg:`#ffffff`,fg:`#d84c00`},
  {pool:`nitin`,text:`DAILY STANDUP`,bg:`#ff9a1f`,fg:`#ffffff`},
  {pool:`nitin`,text:`DEADLINE KAL!`,bg:`#0f7a3a`,fg:`#ffffff`},
  {pool:`mbapu`,text:`CALM DOWN`,bg:`#ffd700`,fg:`#1a1000`},
  {pool:`mbapu`,text:`HR CALLING`,bg:`#ffffff`,fg:`#b8860b`}
];
var It = .45;
var Lt = class{"""

js = js[:idx_ft] + office_placards + js[idx_ft_end + len("Lt=class{"):]


# ==============================================================================
# F. EUC Support Person (formerly Chaiwala: Ni and Pi)
# ==============================================================================
print("F. Updating EUC support person dialogue...")

old_nipi = "var Ni=[`Chai! Chai!`,`Garam chai!`,`Cutting chai, ₹10!`,`Chai le lo, chai!`],Pi=[`Arre! Mera cup!`,`Oye! Chai gira di!`,`Paise kaun dega?!`];"
new_nipi = """var Ni=[
  `Hostname dedo!`,
  `Please raise Elixir ticket for this!`,
  `Naya laptop nhi milega!`,
  `Lunch ke baad aana!`,
  `Restart karke dekha kya?`,
  `Cache clear karo pehle!`
],
Pi=[
  `Arre! Please raise Elixir ticket for this!`,
  `Hostname dedo pehle!`,
  `Oye! Asset tag tod diya!`,
  `Naya laptop nahi milega!`,
  `IT policy violate kar di!`
];"""
assert old_nipi in js, "old_nipi not found"
js = js.replace(old_nipi, new_nipi)


# ==============================================================================
# G. Moving Server Rack instead of Cow Crossing (Ki + announcement)
# ==============================================================================
print("G. Replacing cow crossing with moving server rack (S4 HANA Upgrade)...")

# Announcement
old_cow_say = "o.say(`⚠ COW CROSSING<small>Sab ruk jao!</small>`,`cow`,2600)"
new_cow_say = "o.say(`⚠ S4 HANA UPGRADE IN PROGRESS<small>S4 Hana upgrade going on please wait!</small>`,`cow`,3200)"
assert old_cow_say in js, "old_cow_say not found"
js = js.replace(old_cow_say, new_cow_say)

# Shout speech
old_moo_speech = "this.ctx.hud.speech(r?`ALOO LE LO! PYAAZ LE LO!`:`MOOOOO!`,e.x,e.y,`small`)"
new_moo_speech = "this.ctx.hud.speech(r?`ALOO LE LO! PYAAZ LE LO!`:`S4 HANA UPGRADE GOING ON PLEASE WAIT!`,e.x,e.y,`small`)"
assert old_moo_speech in js, "old_moo_speech not found"
js = js.replace(old_moo_speech, new_moo_speech)

# Moving Server Rack Geometry in Ki()
server_rack_ki = """function Ki(){
  let root = new c;
  let rackMat = new x({ color: 0x18181c, roughness: 0.5, metalness: 0.8 });
  let frame = new p(new C(0.9, 1.85, 0.75), rackMat);
  frame.position.y = 1.05;
  frame.castShadow = true;
  root.add(frame);

  // Perforated front grill / glass door
  let glassDoor = new p(new C(0.82, 1.75, 0.04), new x({ color: 0x112233, roughness: 0.2, metalness: 0.9, transparent: true, opacity: 0.6 }));
  glassDoor.position.set(0, 1.05, 0.38);
  root.add(glassDoor);

  // Server Blades with blinking status LEDs
  let bladeMat = new x({ color: 0x222228, roughness: 0.4, metalness: 0.6 });
  for (let i = 0; i < 9; i++) {
    let blade = new p(new C(0.78, 0.14, 0.65), bladeMat);
    blade.position.set(0, 0.35 + i * 0.175, 0.03);
    root.add(blade);

    let ledColor = (i % 3 === 0) ? 0x00ff88 : (i % 3 === 1) ? 0x00d4ff : 0xff9900;
    let led = new p(new C(0.04, 0.04, 0.02), new g({ color: ledColor }));
    led.position.set(-0.32, 0.35 + i * 0.175, 0.37);
    root.add(led);

    let led2 = new p(new C(0.04, 0.04, 0.02), new g({ color: 0x00ff44 }));
    led2.position.set(-0.25, 0.35 + i * 0.175, 0.37);
    root.add(led2);
  }

  // Marquee Banner on Top with "S4 HANA UPGRADE GOING ON PLEASE WAIT"
  let bannerCanvas = document.createElement("canvas");
  bannerCanvas.width = 512;
  bannerCanvas.height = 96;
  let bctx = bannerCanvas.getContext("2d");
  bctx.fillStyle = "#ffcc00";
  bctx.fillRect(0, 0, 512, 96);
  bctx.fillStyle = "#000000";
  bctx.lineWidth = 6;
  bctx.strokeRect(4, 4, 504, 88);
  bctx.font = "bold 26px sans-serif";
  bctx.textAlign = "center";
  bctx.textBaseline = "middle";
  bctx.fillText("⚠ S4 HANA UPGRADE GOING ON", 256, 32);
  bctx.font = "bold 24px sans-serif";
  bctx.fillStyle = "#d8232a";
  bctx.fillText("PLEASE WAIT!", 256, 68);

  let bannerTex = new _e(bannerCanvas);
  bannerTex.colorSpace = oe;
  bannerTex.needsUpdate = true;
  let bannerMat = new g({ map: bannerTex });
  let bannerFront = new p(new C(1.1, 0.32, 0.05), bannerMat);
  bannerFront.position.set(0, 2.15, 0.39);
  root.add(bannerFront);

  let bannerBack = new p(new C(1.1, 0.32, 0.05), bannerMat);
  bannerBack.position.set(0, 2.15, -0.39);
  bannerBack.rotation.y = Math.PI;
  root.add(bannerBack);

  // 4 Caster Wheels (legs)
  let wheelMat = new x({ color: 0x111111, roughness: 0.8, metalness: 0.5 });
  let wheelRimMat = new x({ color: 0x888888, metalness: 0.9, roughness: 0.2 });
  let legs = [];
  for (let [wx, wz] of [[0.36, 0.3], [-0.36, 0.3], [0.36, -0.3], [-0.36, -0.3]]) {
    let wheelPivot = new c;
    wheelPivot.position.set(wx, 0.12, wz);
    let wheelMesh = new p(new E(0.09, 0.09, 0.06, 16), wheelMat);
    wheelMesh.rotation.z = Math.PI / 2;
    wheelPivot.add(wheelMesh);
    let hub = new p(new E(0.04, 0.04, 0.07, 12), wheelRimMat);
    hub.rotation.z = Math.PI / 2;
    wheelPivot.add(hub);
    root.add(wheelPivot);
    legs.push(wheelPivot);
  }

  // Head: Slide-out IT Diagnostic Console Monitor
  let headPivot = new c;
  headPivot.position.set(0, 1.45, 0.38);
  let monitorScreen = new p(new C(0.52, 0.34, 0.03), new g({ color: 0x00ffcc }));
  monitorScreen.position.set(0, 0, 0.05);
  headPivot.add(monitorScreen);
  root.add(headPivot);

  // Jaw: Slide-out Keyboard tray
  let jawPivot = new c;
  jawPivot.position.set(0, 1.25, 0.38);
  let kbMesh = new p(new C(0.48, 0.03, 0.22), new x({ color: 0x2b2b35 }));
  kbMesh.position.set(0, 0, 0.1);
  jawPivot.add(kbMesh);
  root.add(jawPivot);

  // Tail: Trailing heavy Cat6 / Fiber Optic umbilical cable bundle
  let tailPivot = new c;
  tailPivot.position.set(0, 0.25, -0.4);
  let cableMesh = new p(new E(0.035, 0.045, 0.8, 8), new x({ color: 0x0088ff, roughness: 0.7 }));
  cableMesh.rotation.x = Math.PI / 3;
  cableMesh.position.set(0, -0.15, -0.3);
  tailPivot.add(cableMesh);
  root.add(tailPivot);

  return { root, legs, head: headPivot, tail: tailPivot, jaw: jawPivot };
}
"""

idx_ki = js.find("function Ki(){")
idx_ki_end = js.find("var qi=class", idx_ki)
assert idx_ki != -1, "Ki not found"
js = js[:idx_ki] + server_rack_ki + js[idx_ki_end:]


# ==============================================================================
# H. Corporate Politics Idle Taunts (ji) & Excuses (ki) & Win Headlines (Ai)
# ==============================================================================
print("H. Adding corporate idle taunts, loss excuses, and win headlines...")

# Idle taunts
old_ji_modi = "ji={modi:[`Mitron, main intezaar kar raha hoon!`,`Itna time toh notebandi mein bhi nahi laga!`,`Aao, lamba bhashan sunte hain!`]"
new_ji_modi = "ji={modi:[`Prompt likh raha hu, wait karo!`,`Itna time inference me nahi lagta!`,`Vibe code kar raha hu, interrupt mat karo!`],abdul:[`Ping test chal raha hai, ruko!`,`Packet loss ho raha hai moves me!`,`Jaa pehle Elixir pe SR raise karke aa!`]"
assert old_ji_modi in js, "old_ji_modi not found"
js = js.replace(old_ji_modi, new_ji_modi)

# Loss excuses
old_ki = "ki={modi:[`\"Yeh sab pichhle 70 saal ki galti hai.\" — MitraMan camp`,`\"Opposition ki saazish thi.\" — MitraMan camp`,`\"Hum aatmanirbhar haar se seekhenge.\" — MitraMan camp`]"
new_ki = "ki={modi:[`\"Model hallucinate kar gaya tha.\" — AGM Madhuman camp`,`\"GPU memory out-of-bounds crash ho gayi.\" — AGM Madhuman camp`,`\"Token context window khatam ho gayi thi.\" — AGM Madhuman camp`],abdul:[`\"ISP switch maintenance chal rahi thi.\" — Network Specialist Diby camp`,`\"Packet drop ho gaya tha fight ke beech me.\" — Network Specialist Diby camp`,`\"SR raise nahi hua tha time pe.\" — Network Specialist Diby camp`]"
assert old_ki in js, "old_ki not found"
js = js.replace(old_ki, new_ki)

# Win headlines in Ai
old_headlines = "headline:o?{modi:`MITRAMAN SWEEPS SANSAD!`,rahul:`YATRA BOY WALKS TO VICTORY!`,didi:`DEEDEE STORMS DELHI!`,trump:`TARIFF TAAU TAXES SANSAD!`,yogi:`DOZER DADA FLATTENS SANSAD!`,nitin:`TOLL MAN PAVES OVER SANSAD!`,mbapu:`MBAPU CALMS THE SANSAD!`}[e]:{modi:`MITRAMAN SCRAPES THROUGH!`,rahul:`YATRA BOY WINS THRILLER!`,didi:`DEEDEE SITS ON VICTORY!`,trump:`TARIFF TAAU CLOSES THE DEAL!`,yogi:`DOZER DADA WINS BY A WHISKER!`,nitin:`TOLL MAN WINS IN THE FAST LANE!`,mbapu:`MBAPU WINS WITH SABAR & SHANTI!`}[e]"
new_headlines = "headline:o?{abdul:`NETWORK SPECIALIST DIBY BLOCKS ENTIRE ARENA!`,modi:`AGM MADHUMAN AUTOMATES EVERYONE OUT OF SANSAD!`,rahul:`YATRA BOY WALKS TO VICTORY!`,didi:`DEEDEE STORMS DELHI!`,trump:`TARIFF TAAU TAXES SANSAD!`,yogi:`DOZER DADA FLATTENS SANSAD!`,nitin:`TOLL MAN PAVES OVER SANSAD!`,mbapu:`MBAPU CALMS THE SANSAD!`}[e]:{abdul:`DIBY RESOLVES ALL INCIDENTS WITH A WIN!`,modi:`AGM MADHUMAN VIBE CODES TO VICTORY!`,rahul:`YATRA BOY WINS THRILLER!`,didi:`DEEDEE SITS ON VICTORY!`,trump:`TARIFF TAAU CLOSES THE DEAL!`,yogi:`DOZER DADA WINS BY A WHISKER!`,nitin:`TOLL MAN WINS IN THE FAST LANE!`,mbapu:`MBAPU WINS WITH SABAR & SHANTI!`}[e]"
assert old_headlines in js, "old_headlines not found"
js = js.replace(old_headlines, new_headlines)

# Mastheads
js = js.replace(
    "gi([`THE DAILY JUMLA`,`SANSAD TIMES`,`BREAKING BAKWAS`,`THE KURSI EXPRESS`],r)",
    "gi([`THE ASIAN PAINTS OBSERVER`,`TECH FLOOR CHRONICLES`,`IT ESCALATION TIMES`,`THE ELIXIR TICKET EXPRESS`],r)"
)


# ==============================================================================
# I. Face Photo Texture Mapping (class ls)
# ==============================================================================
print("I. Updating face photo handling in class ls...")

old_setface = "setFacePhoto(){}"
new_setface = """setFacePhoto(e){
  let headObj = this.headMesh;
  if (!headObj) return;
  let tex = new we().load(e, () => {
    tex.flipY = false;
    headObj.traverse(child => {
      if (child.isMesh && child.material) {
        let mats = Array.isArray(child.material) ? child.material : [child.material];
        for (let m of mats) {
          if (m.name && m.name.toLowerCase().includes('head')) {
            m.map = tex;
            m.needsUpdate = true;
          }
        }
      }
    });
  });
}"""
assert old_setface in js, "old_setface not found"
js = js.replace(old_setface, new_setface)

# Hr and Wr roster definitions
js = js.replace("Hr=[`modi`", "Hr=[`abdul`,`modi`")
js = js.replace("Wr={modi:!0", "Wr={abdul:!0,modi:!0")

# Preload abdul model in ud()
old_ud = "let e=[`modi`,`rahul`].filter(e=>Gr.includes(e));"
new_ud = "let e=[`abdul`,`modi`,`rahul`].filter(e=>Gr.includes(e));"
assert old_ud in js, "old_ud not found"
js = js.replace(old_ud, new_ud)


# ==============================================================================
# Save and Verify
# ==============================================================================
with open("public/assets/main-B8x0sGzM.js", "w") as f:
    f.write(js)

print("SUCCESS: public/assets/main-B8x0sGzM.js written successfully! Size:", len(js))

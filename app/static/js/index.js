    console.log("CLEANZO 3D Loaded");


        // Clean, self-contained 3D viewer for the landing page
        console.log('CLEANZO 3D Loaded');

        const container = document.getElementById('car3dViewer');
        if (!container) {
            console.warn('No #car3dViewer container found');
        } else {
            const scene = new THREE.Scene();
            scene.background = null;

            const camera = new THREE.PerspectiveCamera(32, container.clientWidth / container.clientHeight, 0.1, 1000);

            function updateCameraPosition(){
                if(window.innerWidth < 768){
                    camera.position.set(0, 1.1, 9.5);
                } else {
                    camera.position.set(0, 1.3, 11);
                }
                camera.lookAt(0, 0, 0);
            }
            updateCameraPosition();

            const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            // Cap device pixel ratio on mobile to improve performance
            var dpr = window.devicePixelRatio || 1;
            if(window.innerWidth < 992){ dpr = Math.min(dpr, 1); }
            else { dpr = Math.min(dpr, 1.5); }
            renderer.setPixelRatio(dpr);
            renderer.outputEncoding = THREE.sRGBEncoding;
            renderer.toneMapping = THREE.ACESFilmicToneMapping;
            // increase exposure for showroom brightness
            renderer.toneMappingExposure = 1.8;
            // use physically based lighting for more realistic falloff
            renderer.physicallyCorrectLights = true;
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lights
            // Ambient - soft fill for deep shadow areas
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
            scene.add(ambientLight);

            // soft hemisphere for background lighting (keep subtle)
            const hemi = new THREE.HemisphereLight(0x223344, 0x08131d, 1.0);
            scene.add(hemi);

            // Key Light (front-left) - strongest, white, casts shadows
            // Key Light (front-left) - strongest, white, casts shadows
            const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
            keyLight.position.set(6, 5, 5);
            keyLight.castShadow = true;
            keyLight.shadow.mapSize.width = (window.innerWidth < 992) ? 1024 : 2048;
            keyLight.shadow.mapSize.height = (window.innerWidth < 992) ? 1024 : 2048;
            keyLight.shadow.bias = -0.0005;
            scene.add(keyLight);

            // Fill Light (front-right) - softer, reduces harsh shadows
            const fillLight = new THREE.SpotLight(0xffffff, 0.9, 40, Math.PI / 8, 0.6, 1);
            fillLight.position.set(-6, 4, 4);
            fillLight.penumbra = 0.6;
            fillLight.castShadow = false;
            scene.add(fillLight);

            // Top Strip Light (ceiling LED simulation) - narrow, above car
            const topStrip = new THREE.SpotLight(0xffffff, 1.0, 60, Math.PI / 12, 0.7, 1);
            topStrip.position.set(0, 8, 0);
            topStrip.target.position.set(0, 0, 0);
            topStrip.castShadow = false;
            scene.add(topStrip);
            scene.add(topStrip.target);

            // overhead spotlight directly above car to add strong top-down illumination
            const overheadTarget = new THREE.Object3D();
            overheadTarget.position.set(0, 0, 0);
            scene.add(overheadTarget);
            const overheadSpot = new THREE.SpotLight(0xffffff, 12, 200, 0.35, 0.5, 1);
            overheadSpot.position.set(0, 10, 0);
            overheadSpot.target = overheadTarget;
            overheadSpot.castShadow = true;
            overheadSpot.shadow.mapSize.width = (window.innerWidth < 992) ? 1024 : 2048;
            overheadSpot.shadow.mapSize.height = (window.innerWidth < 992) ? 1024 : 2048;
            scene.add(overheadSpot);

            // large rectangular area light above vehicle (showroom ceiling panel)
            try{ if(THREE.RectAreaLightUniformsLib) THREE.RectAreaLightUniformsLib.init(); }catch(e){}
            try{
                const rectArea = new THREE.RectAreaLight(0xffffff, 35, 8, 4);
                rectArea.position.set(0, 6.2, 0);
                rectArea.lookAt(0, 0, 0);
                scene.add(rectArea);
            }catch(e){ /* ignore if RectAreaLight unsupported */ }

            // Rear Rim Light - behind vehicle to highlight silhouette
            const rearRim = new THREE.SpotLight(0xffffff, 0.9, 60, Math.PI / 6, 0.6, 1);
            rearRim.position.set(0, 4, -8);
            rearRim.penumbra = 0.6;
            rearRim.castShadow = false;
            scene.add(rearRim);

            // Blue Accent Light - underbody bounce, stronger for showroom effect
            const blueAccent = new THREE.PointLight(0x3bb7ff, 0.35, 8);
            blueAccent.position.set(0, 1, 0);
            scene.add(blueAccent);

                // Ceiling LED ring (continuous curved LED strip)
                // Suspended ceiling ring placeholder - will be recreated later with correct radius and lights
                const ceilingRing = new THREE.Object3D();
                ceilingRing.position.set(0, 6.2, 0);
                scene.add(ceilingRing);

                // Soft downward glow from ceiling using a subtle point light
                // keep original ceiling glow disabled; we'll provide studio lighting from a dedicated ceiling ring
                const ceilingGlow = new THREE.PointLight(0xcfeeff, 0.0, 40);
                ceilingGlow.position.set(0, 5.8, 0);

            const blueLight = new THREE.PointLight(0x39cfff, 0.0, 60);
            blueLight.position.set(-6, 4, 6);
            scene.add(blueLight);

            const frontLight = new THREE.PointLight(0xffffff, 0.0, 40);
            frontLight.position.set(0, 3, 10);
            scene.add(frontLight);

            const backLight = new THREE.PointLight(0x1d8fff, 0.0, 50);
            backLight.position.set(0, 2, -10);
            scene.add(backLight);

            // Floor
            const floorGeometry = new THREE.CircleGeometry(10.6, 96);
            const floorMaterial = new THREE.MeshStandardMaterial({ color: 0x08131d, metalness: 0.8, roughness: 0.25, transparent: true, opacity: 0.95 });
            const floor = new THREE.Mesh(floorGeometry, floorMaterial);
            floor.rotation.x = -Math.PI / 2;
            floor.position.y = -2.4;
            floor.receiveShadow = true;
            // keep floor hidden to avoid baked glow strips; platform provides the visual anchor
            floor.visible = false;
            scene.add(floor);

            // Rings + physical base plate
            // Platform group: base plate + rings + model will be attached here so they move together
            const platformGroup = new THREE.Group();
            // Add platformGroup to scene early so base/rings render even before model finishes loading
            scene.add(platformGroup);

            // DEBUG helpers (visible guides) - remove when satisfied
            const axes = new THREE.AxesHelper(5);
            axes.visible = false; // set true if you want axes
            scene.add(axes);

            // visible debug ring to validate base position/scale if needed
            const debugRingGeo = new THREE.RingGeometry(2.9, 3.1, 64);
            const debugRingMat = new THREE.MeshBasicMaterial({ color: 0xff3333, side: THREE.DoubleSide, transparent: true, opacity: 0.15 });
            const debugRing = new THREE.Mesh(debugRingGeo, debugRingMat);
            debugRing.rotation.x = -Math.PI / 2;
            debugRing.position.y = -1.6;
            debugRing.visible = false; // keep debug ring hidden in production
            scene.add(debugRing);

            // expose debug helpers for quick console toggling
            window.platformGroup = platformGroup;
            window.debugRing = debugRing;
            window.debugAxes = axes;

            // Base plate (unit cylinder, will scale to match car footprint after model loads)
            const plateHeight = 0.28;
            const baseGeo = new THREE.CylinderGeometry(1, 1, plateHeight, 128);
            // darker, glossier showroom floor
            const baseMat = new THREE.MeshStandardMaterial({ color: 0x07121a, metalness: 0.9, roughness: 0.18 });
            const basePlate = new THREE.Mesh(baseGeo, baseMat);
            // initial scale; will be adjusted after loading model
            basePlate.scale.set(6.0, 1, 3.5);
            // place slightly below rings by default
            basePlate.position.y = -1.75;
            basePlate.receiveShadow = true;
            platformGroup.add(basePlate);

            // Top core disk (dark tiles with subtle emissive core beneath)
            const coreGeo = new THREE.CircleGeometry(1, 128);
            const coreTopMat = new THREE.MeshStandardMaterial({ color: 0x0b1114, metalness: 0.9, roughness: 0.12 });
            const coreTop = new THREE.Mesh(coreGeo, coreTopMat);
            coreTop.rotation.x = -Math.PI / 2;
            // will position/scale after model loads
            coreTop.position.y = basePlate.position.y + (plateHeight / 2) + 0.01;
            coreTop.receiveShadow = true;
            platformGroup.add(coreTop);

            // removed baked/giant core glow to avoid white disk artifacts
            const coreGlowMat = new THREE.MeshBasicMaterial({ color: 0x9be8ff, transparent: true, opacity: 0.6, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
            const coreGlow = new THREE.Mesh(coreGeo, coreGlowMat);
            coreGlow.visible = false;

            // thin neon edge ring at top of base (for rim illumination) - subtle blue LED edge
            const neonEdgeGeo = new THREE.TorusGeometry(1.0, 0.04, 16, 200);
            const neonEdgeMat = new THREE.MeshStandardMaterial({ color: 0x0f6fb0, emissive: 0x0f6fb0, emissiveIntensity: 1.8, metalness: 0.1, roughness: 0.18, side: THREE.DoubleSide });
            const neonEdge = new THREE.Mesh(neonEdgeGeo, neonEdgeMat);
            neonEdge.rotation.x = Math.PI / 2;
            neonEdge.position.y = basePlate.position.y + (plateHeight / 2) - 0.01;
            neonEdge.visible = true;
            platformGroup.add(neonEdge);

            // Blue LED ring light around platform to illuminate platform surface
            const platformBlue = new THREE.PointLight(0x3bb7ff, 2.5, 8);
            platformBlue.position.set(0, basePlate.position.y + (plateHeight/2) + 0.01, 0);
            scene.add(platformBlue);

            // Soft floor bounce light from below the platform
            const floorBounce = new THREE.PointLight(0x3bb7ff, 2.0, 10);
            floorBounce.position.set(0, basePlate.position.y - 0.6, 0);
            scene.add(floorBounce);

            const ringOuterGeo = new THREE.TorusGeometry(9.4, 0.22, 64, 400);
    const ringOuterMat = new THREE.MeshStandardMaterial({
        color: 0x2aa8d9,
        emissive: 0x2aa8d9,
        emissiveIntensity: 0.6,
        transparent: true,
        opacity: 0.95,
        side: THREE.DoubleSide
    });
    // remove the outer torus ring (avoid large white/colored torus artifacts)
    const ringOuterMesh = new THREE.Mesh(ringOuterGeo, ringOuterMat);
    ringOuterMesh.rotation.x = Math.PI / 2;
    ringOuterMesh.position.y = -1.45;
    ringOuterMesh.visible = false;



    const ringInnerGeo = new THREE.TorusGeometry(7.4, 0.18, 64, 400);
    const ringInnerMat = new THREE.MeshStandardMaterial({
        color: 0x1778b8,
        emissive: 0x1778b8,
        emissiveIntensity: 0.6,
        transparent: true,
        opacity: 0.95,
        side: THREE.DoubleSide
    });
    // remove the inner torus ring
    const ringInnerMesh = new THREE.Mesh(ringInnerGeo, ringInnerMat);
    ringInnerMesh.rotation.x = Math.PI / 2;
    ringInnerMesh.position.y = -1.42;
    ringInnerMesh.visible = false;

    // Rings are visible LED elements on the platform
            // Removed legacy rings. Build a proper circular showroom environment now.
            (function buildShowroom(){
                const wallRadius = 12;
                const wallHeight = 6.0;
                const wallGeo = new THREE.CylinderGeometry(wallRadius, wallRadius, wallHeight, 64, 1, true);
                const wallMat = new THREE.MeshStandardMaterial({ color: 0x061015, metalness: 0.7, roughness: 0.36, side: THREE.BackSide });
                const walls = new THREE.Mesh(wallGeo, wallMat);
                walls.position.y = -1.4;
                scene.add(walls);

                // Vertical LED bars around the wall (subtle blue-white accents)
                const ledCount = 12;
                for(let i=0;i<ledCount;i++){
                    const ang = (i/ledCount) * Math.PI * 2;
                    const x = Math.cos(ang) * (wallRadius - 0.5);
                    const z = Math.sin(ang) * (wallRadius - 0.5);
                    const barGeo = new THREE.BoxGeometry(0.12, 4.0, 0.08);
                    const barMat = new THREE.MeshStandardMaterial({ color: 0x9be8ff, emissive: 0x9be8ff, emissiveIntensity: 1.0, metalness: 0.0, roughness: 0.25 });
                    const bar = new THREE.Mesh(barGeo, barMat);
                    bar.position.set(x, 0.6, z);
                    bar.lookAt(0, bar.position.y, 0);
                    scene.add(bar);
                    // small point light to provide local bounce
                    const p = new THREE.PointLight(0x9be8ff, 0.25, 6);
                    p.position.set(x, 1.0, z);
                    scene.add(p);
                }

                // Ceiling LED ring - suspended, blue-white, radius ~9
                const ceilingRingGeo = new THREE.TorusGeometry(9.0, 0.12, 24, 256);
                const ceilingRingMat = new THREE.MeshStandardMaterial({ color: 0x9be8ff, emissive: 0x9be8ff, emissiveIntensity: 1.4, metalness: 0.0, roughness: 0.12, side: THREE.DoubleSide });
                const ceilingRingMesh = new THREE.Mesh(ceilingRingGeo, ceilingRingMat);
                ceilingRingMesh.rotation.x = Math.PI / 2;
                ceilingRingMesh.position.y = 5.6;
                scene.add(ceilingRingMesh);

                // Add downward spotlights attached to the ceiling ring to illuminate roof/bonnet
                const spotCount = 6;
                for(let j=0;j<spotCount;j++){
                    const a = (j/spotCount) * Math.PI * 2;
                    const sx = Math.cos(a) * 9.0;
                    const sz = Math.sin(a) * 9.0;
                    const sp = new THREE.SpotLight(0xffffff, 1.2, 40, Math.PI/10, 0.3, 1);
                    sp.position.set(sx, 5.6, sz);
                    sp.target.position.set(0, 0.2, 0);
                    sp.castShadow = true;
                    scene.add(sp);
                    scene.add(sp.target);
                }
            })();

            // Add a soft underglow beneath the car (blue lights) to emphasize contact
            // underglow beneath wheels - disable to remove bright patches near tyres
            const underGlowLeft = new THREE.PointLight(0x39cfff, 0.0, 8);
            underGlowLeft.position.set(-1.8, -1.0, 0.8);
            scene.add(underGlowLeft);

            const underGlowRight = new THREE.PointLight(0x39cfff, 0.0, 8);
            underGlowRight.position.set(1.8, -1.0, 0.8);
            scene.add(underGlowRight);

            // Add subtle rim lights (from back-left and back-right) to accent edges
            // rim lights - keep subtle
            const rimLeft = new THREE.DirectionalLight(0x74d6ff, 0.2);
            rimLeft.position.set(-8, 4, -6);
            scene.add(rimLeft);

            const rimRight = new THREE.DirectionalLight(0x74d6ff, 0.2);
            rimRight.position.set(8, 4, -6);
            scene.add(rimRight);

            // Controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableZoom = false;
            controls.enablePan = false;
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            // We'll animate platformGroup explicitly (left-right). Keep controls for drag only.
            controls.autoRotate = false;
            controls.minPolarAngle = Math.PI / 2.15;
            controls.maxPolarAngle = Math.PI / 2.15;
            // ensure controls target focuses on platform center
            controls.target.set(0, -1.4, 0);
            controls.update();

            // Load model
            const loader = new THREE.GLTFLoader();
            loader.load(
                '/static/models/car.glb',
                function(gltf){
                    console.log('MODEL LOADED');
                    const model = gltf.scene;
                    // Diagnostic: list all meshes and their material properties (no changes)
                    try{
                        model.traverse(function(child){
                            if(child.isMesh && child.material){
                                try{
                                    const mat = child.material;
                                    const matName = mat.name || '(noname)';
                                    const meshName = child.name || '(noname)';
                                    let colorHex = null;
                                    if(mat.color && typeof mat.color.getHexString === 'function'){
                                        colorHex = '#' + mat.color.getHexString();
                                    }
                                    const metalness = (mat.metalness !== undefined) ? mat.metalness : null;
                                    const roughness = (mat.roughness !== undefined) ? mat.roughness : null;
                                    const envMapIntensity = (mat.envMapIntensity !== undefined) ? mat.envMapIntensity : null;
                                    console.log('MESH:', meshName, 'MATERIAL:', matName, 'color:', colorHex, 'metalness:', metalness, 'roughness:', roughness, 'envMapIntensity:', envMapIntensity);
                                }catch(e){ /* ignore per-mesh logging errors */ }
                            }
                        });
                    }catch(e){ console.warn('Material diagnostic failed', e); }
                    // compute size and apply scale first
                    const size = new THREE.Box3().setFromObject(model).getSize(new THREE.Vector3());
                    const maxAxis = Math.max(size.x, size.y, size.z) || 1;
                    const modelScale = (window.innerWidth < 768) ? (6 / maxAxis) : (3.2 / maxAxis);
                    model.scale.setScalar(modelScale);
                    // apply a facing rotation
                    model.rotation.y = Math.PI * 0.95;

                    // recompute bounding box after scale & rotation
                    const box2 = new THREE.Box3().setFromObject(model);
                    const minY = box2.min.y;

                    // position base plate (depends on model footprint) before grounding the model
                    const footprintX = box2.getSize(new THREE.Vector3()).x;
                    const footprintZ = box2.getSize(new THREE.Vector3()).z;
                    const footprint = Math.max(footprintX, footprintZ);
                    // desired base radius should be slightly larger than half the footprint
                    const looseRadius = Math.max(footprint * 0.48, 2.2);
                    const desiredRadius = Math.min(looseRadius, 4.2);
                    basePlate.scale.set(desiredRadius, 1, desiredRadius);

                    // ring height reference (unchanged) and compute base top target
                    const ringHeight = -1.45;
                    const baseTopTargetY = ringHeight - 0.02;
                    basePlate.position.y = baseTopTargetY - (plateHeight / 2);

                    // compute top Y of base (flat surface)
                    const baseTopY = basePlate.position.y + (plateHeight / 2);

                    // A) Recalculate model bounding box after scaling/rotation (we already have box2)
                    // B) Position the model so the lowest point (tyre) sits exactly on baseTopY
                    const desiredTyreY = baseTopY; // per spec: desiredTyreY = basePlate.position.y + (plateHeight/2)
                    // adjust model so that boundingBox.min.y == desiredTyreY
                    const adjust = desiredTyreY - minY;
                    model.position.y = (model.position.y || 0) + adjust;
                    // recompute to verify
                    const postBox = new THREE.Box3().setFromObject(model);
                    const postMinY = postBox.min.y;
                    console.log('Base Top Y:', baseTopY);
                    console.log('Model Min Y:', postMinY);
                    console.log('Tyre Contact Fixed');
                    // coreTop: slightly smaller than base to show top tiles
                    coreTop.scale.set(desiredRadius * 0.96, 1, desiredRadius * 0.96);
                    coreTop.position.y = baseTopY + 0.008;
                    // coreGlow: inner emissive disk a bit smaller
                    coreGlow.scale.set(desiredRadius * 0.7, 1, desiredRadius * 0.7);
                    coreGlow.position.y = baseTopY + 0.004;
                    // neon edge: slightly larger than base top to produce rim highlight
                    neonEdge.scale.set(desiredRadius * 1.02, 1, desiredRadius * 1.02);
                    neonEdge.position.y = baseTopY - 0.01;

                    // Additional safety: hide any large thin flat meshes (ribbon-like) near baseTopY
                    model.traverse(function(child){
                        if(child.isMesh){
                            try{
                                const cb = new THREE.Box3().setFromObject(child);
                                const sizeC = cb.getSize(new THREE.Vector3());
                                const centerC = cb.getCenter(new THREE.Vector3());
                                // heuristics: relatively thin in Y, wide in X/Z, and centered near the base top
                                const thinY = sizeC.y < Math.max(1.0, (plateHeight * 4.0));
                                const wideEnough = (sizeC.x > (desiredRadius * 0.3)) || (sizeC.z > (desiredRadius * 0.3));
                                const nearBase = Math.abs(centerC.y - baseTopY) < 0.6;
                                // also check material brightness if available
                                let bright = false;
                                if(child.material){
                                    try{
                                        const col = child.material.color ? child.material.color : null;
                                        const emiss = child.material.emissive ? child.material.emissive : null;
                                        const br = (col ? (col.r + col.g + col.b)/3 : 0) + (emiss ? (emiss.r + emiss.g + emiss.b)/3 : 0);
                                        if(br > 0.6) bright = true;
                                    }catch(e){}
                                }
                                if(thinY && wideEnough && nearBase && bright){
                                    child.visible = false;
                                    console.log('Hiding ribbon-like child:', child.name || '(noname)', 'size:', sizeC, 'centerY:', centerC.y);
                                }
                            }catch(e){ /* ignore */ }
                        }
                    });

                    // stronger removal: hide meshes whose material color/emissive is close to pale cyan
                    function hexToRgb(hex){
                        const h = (typeof hex === 'number') ? hex : parseInt(hex.replace('#',''),16);
                        return { r: ((h >> 16) & 255)/255, g: ((h >> 8) & 255)/255, b: (h & 255)/255 };
                    }
                    function colorDist(a,b){
                        return Math.sqrt(Math.pow(a.r-b.r,2)+Math.pow(a.g-b.g,2)+Math.pow(a.b-b.b,2));
                    }
                    const target = hexToRgb(0xbfe9ff);
                    const NAME_KEYWORDS = ['ribbon','band','path','stripe','skirt','under','ring','plate','tube'];
                    model.traverse(function(child){
                        if(child.isMesh && child.material){
                            try{
                                const name = (child.name||'').toLowerCase();
                                const mat = child.material;
                                let colRgb = null; let emissRgb = null;
                                if(mat.color) colRgb = hexToRgb(mat.color.getHex());
                                if(mat.emissive) emissRgb = hexToRgb(mat.emissive.getHex());

                                let hide = false;
                                if(colRgb){
                                    const d = colorDist(colRgb, target);
                                    if(d < 0.32) hide = true;
                                }
                                if(!hide && emissRgb){
                                    const de = colorDist(emissRgb, target);
                                    if(de < 0.32) hide = true;
                                }
                                if(!hide){
                                    for(const k of NAME_KEYWORDS) if(name.includes(k)) { hide = true; break; }
                                }
                                if(hide){ child.visible = false; console.log('Hiding child by color/name:', child.name || '(noname)', 'matColor:', mat.color?mat.color.getHexString():null, 'emissive:', mat.emissive?mat.emissive.getHexString():null); return; }
                                // otherwise apply showroom tweaks
                                mat.metalness = Math.min((mat.metalness || 0) + 0.2, 1);
                                mat.roughness = Math.max((mat.roughness || 0) - 0.12, 0);
                                child.castShadow = true;
                                child.receiveShadow = true;
                            }catch(e){ /* ignore per-mesh errors */ }
                        }
                    });

                        // After model is scaled/rotated, add dynamic environment reflections
                        // Create cube camera for dynamic env map
                        const cubeRenderTarget = new THREE.WebGLCubeRenderTarget((window.innerWidth < 992) ? 128 : 256, { encoding: THREE.sRGBEncoding });
                        const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
                        // position cubeCamera at model's world center (approx)
                        const modelWorldPos = new THREE.Vector3();
                        model.getWorldPosition(modelWorldPos);
                        cubeCamera.position.copy(modelWorldPos);
                        scene.add(cubeCamera);

                        // apply environment map and enforce showroom PBR values per user's request
                        model.traverse(function(child){
                            if(child.isMesh && child.material){
                                const mat = child.material;
                                // apply the dynamic envMap for reflections
                                mat.envMap = cubeRenderTarget.texture;
                                // For MeshStandardMaterial instances, enforce requested values (preserve color)
                                try{
                                    if(mat.isMeshStandardMaterial || (mat.type && mat.type.indexOf('Standard')>=0)){
                                        const prev = {metalness: mat.metalness, roughness: mat.roughness, envMapIntensity: mat.envMapIntensity};
                                        mat.envMapIntensity = 3.0;
                                        mat.metalness = 0.9;
                                        mat.roughness = 0.2;
                                        console.log('MATERIAL:', mat.name || '(noname)', 'metalness:', prev.metalness, '->', mat.metalness, 'roughness:', prev.roughness, '->', mat.roughness, 'envMapIntensity:', (prev.envMapIntensity!==undefined?prev.envMapIntensity:'(unset)'), '->', mat.envMapIntensity);
                                    }else{
                                        // still print diagnostics for non-standard materials
                                        console.log('MATERIAL:', mat.name || '(noname)', 'metalness:', mat.metalness, 'roughness:', mat.roughness, 'envMapIntensity:', (mat.envMapIntensity !== undefined) ? mat.envMapIntensity : '(unset)');
                                        // set envMapIntensity reasonably
                                        if((mat.envMapIntensity===undefined) || (mat.envMapIntensity < 1.5)) mat.envMapIntensity = 1.6;
                                    }
                                }catch(e){ /* ignore per-material errors */ }
                                mat.needsUpdate = true;
                            }
                        });

                        // additional pass: hide dark, thin, wide meshes that are baked shadows (oval under tyres)
                        model.traverse(function(child){
                            if(child.isMesh){
                                const name = (child.name||'').toLowerCase();
                                if(name.includes('shadow') || name.includes('ground') || name.includes('projection') || name.includes('proj') || name.includes('ellipse') || name.includes('plane') || name.includes('under')){
                                    child.visible = false;
                                    console.log('Hiding child by shadow-name:', child.name);
                                    return;
                                }
                                try{
                                    const bb = new THREE.Box3().setFromObject(child);
                                    const s = bb.getSize(new THREE.Vector3());
                                    const c = bb.getCenter(new THREE.Vector3());
                                    const thin = s.y < 0.12;
                                    const wideEnough = (s.x > (desiredRadius * 0.25)) || (s.z > (desiredRadius * 0.25));
                                    const nearBase = (c.y < baseTopY + 0.6) && (c.y > baseTopY - 1.2);
                                    // brightness (color + emissive average)
                                    let br = 1.0;
                                    if(child.material){
                                        try{
                                            const col = child.material.color; const em = child.material.emissive;
                                            const cr = col ? (col.r + col.g + col.b)/3 : 0;
                                            const er = em ? (em.r + em.g + em.b)/3 : 0;
                                            br = cr + er;
                                        }catch(e){}
                                    }
                                    if(thin && wideEnough && nearBase && br < 0.25){
                                        child.visible = false;
                                        console.log('Hiding shadow-like child:', child.name || '(noname)', 'size:', s, 'centerY:', c.y, 'brightness:', br);
                                    }
                                }catch(e){ /* ignore per-child errors */ }
                            }
                        });

                        // create subtle tyre contact shadows at approximate wheel positions
                        try{
                            const worldBox = new THREE.Box3().setFromObject(model);
                            const worldCenter = worldBox.getCenter(new THREE.Vector3());
                            const worldSize = worldBox.getSize(new THREE.Vector3());
                            const wheelOffsetX = worldSize.x * 0.35;
                            const wheelOffsetZ = worldSize.z * 0.35;
                            const wheelY = worldBox.min.y + 0.005; // just above platform
                            const contactMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.28, depthWrite: false });
                            const contactR = Math.max(worldSize.x * 0.12, 0.18);
                            const contactGeo = new THREE.CircleGeometry(contactR, 32);
                            const wheelOffsets = [
                                new THREE.Vector3(worldCenter.x + wheelOffsetX, wheelY, worldCenter.z + wheelOffsetZ),
                                new THREE.Vector3(worldCenter.x - wheelOffsetX, wheelY, worldCenter.z + wheelOffsetZ),
                                new THREE.Vector3(worldCenter.x + wheelOffsetX, wheelY, worldCenter.z - wheelOffsetZ),
                                new THREE.Vector3(worldCenter.x - wheelOffsetX, wheelY, worldCenter.z - wheelOffsetZ)
                            ];
                            for(const wp of wheelOffsets){
                                // convert world pos to platformGroup local
                                const localPos = platformGroup.worldToLocal(wp.clone());
                                const cs = new THREE.Mesh(contactGeo, contactMat.clone());
                                cs.rotation.x = -Math.PI/2;
                                cs.position.copy(localPos);
                                // place contact shadows slightly below tyre contact point
                                cs.position.y = baseTopY - 0.002; // sit slightly below platform surface
                                cs.renderOrder = 999;
                                platformGroup.add(cs);
                            }
                        }catch(e){ console.warn('Contact shadows setup failed', e); }

                        // attach model to the platform group so it rotates with the base
                        platformGroup.add(model);
                        scene.add(platformGroup);

                        // update cube camera once to capture scene reflections, and expose for periodic updates
                        cubeCamera.update(renderer, scene);
                        window._cubeCamera = cubeCamera;
                        window._cubeCameraCounter = 0;
                        window._cubeCameraUpdateInterval = 12; // update every 12 frames
                    console.log('CAR READY');
                },
                function(xhr){ if(xhr.total) console.log('Loading:', Math.round(xhr.loaded / xhr.total * 100) + '%'); },
                function(error){ console.error('MODEL ERROR:', error); }
            );

            // Animation: continuous 360° rotation of platformGroup (turntable)
            const clock = new THREE.Clock();
            const rotationPeriod = 30.0; // seconds per full revolution

            function animate(){
                requestAnimationFrame(animate);
                const delta = clock.getDelta();
                // rotation speed (radians per second)
                const rotationSpeed = (2 * Math.PI) / rotationPeriod;
                if (typeof platformGroup !== 'undefined') {
                    platformGroup.rotation.y += rotationSpeed * delta;
                    // subtle ring spin for visual interest
                    if (typeof platformGroup !== 'undefined') {
        platformGroup.rotation.y += rotationSpeed * delta;
    }

                }
                controls.update();
                // Periodically update cube camera to refresh dynamic envMap reflections
                try{
                    if(window._cubeCamera){
                        window._cubeCameraCounter = (window._cubeCameraCounter||0) + 1;
                        if(window._cubeCameraCounter % window._cubeCameraUpdateInterval === 0){
                            const center = new THREE.Vector3();
                            platformGroup.getWorldPosition(center);
                            window._cubeCamera.position.copy(center);
                            window._cubeCamera.update(renderer, scene);
                        }
                    }
                }catch(e){/* ignore cube camera update errors */}
                renderer.render(scene, camera);
            }
            animate();

            // Responsive
            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
                updateCameraPosition();
            });
        }
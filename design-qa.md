# Design QA

## Evidence

- Source: `C:\Users\Lab User\.codex\generated_images\01a04f2c-257c-7212-b977-3286ff48c0e6\exec-59977878-4fb0-4724-b277-49f7907419e7.png`
- Final desktop implementation: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-final-1487x1058.png`
- Final mobile implementation: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-final-mobile-390x844.png`
- Full-page implementation: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-final-full-page-v2.png`
- Source and implementation comparison: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-final-comparison.png`
- Previous/revised 3D comparison: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-comparison.png`
- Revised hero: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-hero-desktop.png`
- Revised hero at 55.8% disassembly: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-hero-disassembled.png`
- Revised project gallery, centered state: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-gallery-desktop.png`
- Revised project gallery, next-card state: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-gallery-wheel.png`
- Revised mobile project gallery: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-gallery-mobile.png`
- Compact-card source truth, desktop: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-gallery-desktop.png`
- Compact-card implementation, desktop: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-compact-gallery-desktop.png`
- Compact-card source truth, mobile: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-3d-gallery-mobile.png`
- Compact-card implementation, mobile: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-compact-gallery-mobile.png`
- Landscape-card source truth, desktop: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-compact-gallery-desktop.png`
- Landscape-card implementation, desktop: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-landscape-gallery-desktop.png`
- Landscape-card source truth, mobile: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-compact-gallery-mobile.png`
- Landscape-card implementation, mobile: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\revision-landscape-gallery-mobile.png`
- Desktop viewport: 1487 x 1058 CSS pixels at device scale factor 1
- Mobile viewport: 390 x 844 CSS pixels at device scale factor 1
- State: initial page load, first project centered, assembled mechanical core
- Compact-card comparison normalization: desktop source and implementation are both 1487 x 1058 px at a 1487 x 1058 CSS viewport and device scale factor 1; mobile source and implementation are both 390 x 844 px at a 390 x 844 CSS viewport and device scale factor 1. The centered Ekua card is the shared interaction state.
- Landscape-card comparison normalization: the compact source and landscape implementation use the same 1487 x 1058 desktop and 390 x 844 mobile CSS viewports at device scale factor 1. Both comparisons hold the first Ekua project in the centered, assembled coverflow state.

## Fidelity review

- Typography: The hero headline uses Instrument Sans at its full `wdth: 100` axis, with no horizontal scaling or font stretch. It holds the intended three-line desktop composition with no overflow and a normal-width, lighter display weight.
- Spacing and layout: The graphite hero, curved warm transition, restrained navigation, wide editorial measures, sharp ruled surfaces, and cobalt accent preserve the approved byLarch-inspired visual language.
- Information architecture: The user-requested order is now Hero, About, Tools and systems, Projects, Experience, and Contact. About begins immediately after the hero. The project archive heading now precedes the gallery.
- Project presentation: The former Selected work, category switch, and A closer look blocks are removed. One larger coverflow contains all 24 software, research, robotics, and physical projects, with project-specific context, stack, summary, and links.
- 3D perspective revision: The mechanical core now uses a real look-at camera and perspective projection from above and to the viewer's right. The previous underside-biased object rotation is gone; top planes, front edges, and the exploded vertical axis now share one coherent three-quarter view.
- Cover Flow revision: The pre-redesign 15-degree shelf rotation, 0.82-to-1.08 scale curve, -60-to-80 px depth, 60 px lateral shift, 0-to-0.5 darkening, 150 ms transform timing, and 100 ms wheel cadence are restored. The richer current cards remain, but the desktop center footprint is reduced from roughly 623 x 688 px in the prior implementation capture to 543 x 654 px.
- Compact-card revision: The centered desktop card keeps its 543 px visual width while dropping from 654 px to 580 px in visual height. Mobile drops from 605 px to 531 px. Header padding, metadata wrapping, description padding, and image depth were compacted together, so the reduction comes from removing dead space rather than shrinking the project imagery or deleting details.
- Landscape-card revision: The second reduction keeps the centered visual width fixed at 543 px on desktop and 385 px on mobile while cutting visual height from 580 px to 481 px and from 531 px to 444 px respectively. The header and summary become compact two-column rows around a 2.35:1 media window. The side-by-side visual comparison confirms the image remains legible, metadata and summary copy remain complete, links retain clear targets, and no new clipping or awkward empty regions appear.
- Assets: About uses the real Cursor Hackathon portrait. Ekua, EdgeHarness, temporal roadside calibration, SwipeLease, Clawmsy, and LiveClaw use public first-party product or repository imagery; large new raster assets were resized and encoded as WebP where appropriate.
- Intentional variance from the approved source: The source placed cards in the hero transition. The implementation moves the entire archive below About and the technical section because the user explicitly requested that hierarchy. The original abstract blue sculpture is replaced with an interactive mechanical compute core.

## Interaction and accessibility review

- Navigation: About, Projects, Experience, and Contact anchors work on desktop and through the mobile full-screen menu. Anchor headings clear the fixed header.
- Project coverflow: Wheel, pointer drag, scroll snap, Previous/Next, ArrowLeft/ArrowRight, Home, and End behavior remain intact. The automated flow moved the centered index 0 -> 1 by wheel, 1 -> 2 by Next, 2 -> 1 by keyboard, and 1 -> 2 by drag.
- Compact-card interaction recheck: With the new dimensions, the centered index moved 0 -> 1 by Next, 1 -> 2 by wheel, and 2 -> 3 by drag. All 24 cards remained present; no card, header, or body content overflow was detected at desktop or mobile widths.
- Landscape-card interaction recheck: The final dimensions repeat the 0 -> 1 Next, 1 -> 2 wheel, and 2 -> 3 drag path with the original centered `translate3d(0px, 0px, 80px) rotateY(0deg) scale(1.08)` state intact. All 24 cards measure uniformly at 390 px base height on desktop and 360 px on mobile; card, header, and body overflow checks are empty in both viewports.
- Skills: All five discipline tabs support click and arrow-key selection; active tabs and panels update `aria-selected` and `aria-hidden` correctly.
- Engineering work: All three hardware cards remain in the main archive and open their existing detail dialogs; Escape closes the dialog.
- Contact: LinkedIn, GitHub, email, and resume icon links resolve correctly. The local resume returned HTTP 200 as `application/pdf`.
- Responsive layout: Desktop and 390 px mobile passed with document width equal to viewport width and no horizontal overflow.
- Reduced motion: The WebGL loop stops, the mechanical core renders statically, and coverflow transforms are disabled.
- Diagnostics: No console warnings, console errors, or page errors were observed in desktop, mobile, interaction, modal, or reduced-motion states.

## Rendering and performance review

- Renderer: Real WebGL on ANGLE / Direct3D 11 using the Qualcomm Adreno X1-85 GPU, requested with `powerPreference: high-performance`.
- Animation architecture: The signal field and mechanical assembly use two GPU draw calls. Geometry is allocated once in static buffers; time, pointer position, and disassembly progress are passed as shader uniforms.
- Projection architecture: Camera position, target, basis vectors, perspective divide, view direction, lighting, and depth are calculated in the vertex/fragment shaders. Scroll changed the measured disassembly uniform from 0.037 to 0.558 while the hero remained in view.
- Geometry: 20,688 line vertices and 1,764 mechanical vertices on desktop; the mechanical mesh is disabled below 700 px while the lower-density field remains active.
- Frame sample: 179 requestAnimationFrame intervals averaged 11.11 ms with a 11.20 ms p95 in the installed Chrome fallback environment.
- Main-thread sample: one layout during the measured interval, 21 style recalculations, 0.025 seconds of script time, and about 10.2 MB JavaScript heap usage.
- Image behavior: The coverflow loads only the centered card and nearby project imagery, then progressively loads additional cards as the archive advances.

## Comparison history

1. The first revision exposed the exact issues identified by the user: compressed headline typography, gallery-before-heading order, duplicated featured work, and About too low in the page.
2. The page was rebuilt around the corrected hierarchy, a full-width headline axis, one complete project archive, a concise photo-led About section, and direct contact links.
3. Browser QA found that `content-visibility` caused below-fold sections to disappear from full-page capture. That optimization was removed, and the final full-page pass confirms Experience and Contact render continuously.
4. The final side-by-side comparison confirms the source's graphite, bone, cobalt, editorial typography, curved transition, and spatial depth remain intact while incorporating the requested content and interaction changes.
5. The 3D revision comparison confirms the hero now reads from a consistent top-front viewer position and the project shelf once again has clear rotation, depth compression, overlap, and light falloff while using a smaller center card.
6. The compact-card comparison found the remaining vertical excess inside the header, 16:9 media slot, and description row. Those regions were tightened as one system, then recaptured at matching desktop and mobile states. The post-fix evidence shows a roughly 11% shorter desktop card and 12% shorter mobile card with unchanged width, intact copy, no overflow, and no P0/P1/P2 visual findings. Focused card-region comparison was used because the full-page view was not detailed enough to judge internal padding and wrapping.
7. The landscape-card comparison placed the compact and final captures together at identical viewports. The final card is another 17% shorter on desktop and 16% shorter on mobile, with unchanged visual width, a clearer horizontal reading order, complete content, preserved image subjects, and no P0/P1/P2 findings. The original coverflow depth, overlap, and input behavior remain unchanged.

## Ekua and spacing-system revision

### Current-run evidence

- Desktop source truth before the spacing revision: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-before-full-desktop.png`
- Desktop implementation after the spacing revision: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-after-full-desktop.png`
- Focused Projects source truth: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-before-projects-desktop.png`
- Focused Projects implementation: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-after-projects-desktop.png`
- Mobile source truth before the spacing revision: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-before-full-mobile.png`
- Mobile implementation after the spacing revision: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-after-full-mobile.png`
- User-screenshot-equivalent implementation: `C:\Users\Lab User\AppData\Local\Temp\portfolio-build-20260829\captures\spacing-audit-after-projects-user-viewport.png`
- Ekua repository screenshot source: `C:\Users\Lab User\AppData\Local\Temp\ekua-outreach-source-20260829\demo\4c_sessions_status.png`
- Ekua repository URL: `https://github.com/22joshlee/ekua-outreach`
- Normalization: the desktop before/after captures use a 1487 x 1058 CSS viewport at device scale factor 1; the mobile before/after captures use a 390 x 844 CSS viewport at device scale factor 1. The exact user screenshot shape was rechecked at a 1455 x 747 CSS viewport and device scale factor 2, producing 2910 x 1494 output pixels. All focused project comparisons hold Ekua at center index 0.

### Findings and fixes

- [P1, content and image fidelity] The prior Ekua card represented the public WhatsApp product rather than the supplied `ekua-outreach` project. It used unrelated imagery, product context, stack, copy, and a live-site link. The implementation now uses the repository's real Active Outreach Sessions capture, describes the human-in-the-loop company-research, drafting, reply-management, and scheduling flow, lists Python, FastAPI, and Supabase, and links to the supplied repository. The source repository is private, so unauthenticated visitors will receive GitHub's normal 404 until access or visibility changes.
- [P1, spacing and layout rhythm] Desktop section padding varied from roughly 119 px to 164 px, mobile sections used 96 px, and heading-to-content gaps independently ranged from 58 px to 110 px. Projects compounded a 96 px heading margin with 48 px of gallery padding, visually detaching the archive from its heading. One shared section-space token now resolves to about 100 px on the measured desktop and 64 px on mobile; one heading-content token resolves to 59 px and 40 px respectively. Projects uses a 30 px desktop / 20 px mobile heading-to-gallery gap, with the centered card beginning 57 px / 43 px after the intro.
- [P2, component density] Skill-stage padding and gaps, experience-row padding and column gaps, contact spacing, and coverflow track padding were all independently oversized. Those values now share the tighter cadence. Every skill panel was opened at desktop and mobile widths; all five have zero measured overflow after the mobile density correction.

### Final comparison

- Overall desktop document height fell from 5,464 px to 4,709 px, a 755 px (13.8%) reduction without deleting any section or project.
- Overall mobile document height fell from 6,434 px to 5,735 px, a 699 px (10.9%) reduction.
- Desktop section heights changed as follows: About 737 -> 658 px, Tools 945 -> 809 px, Projects 1,216 -> 978 px, Experience 1,148 -> 923 px, and Contact 460 -> 384 px.
- Mobile section heights changed as follows: About 981 -> 909 px, Tools 1,245 -> 1,050 px, Projects 1,015 -> 872 px, Experience 1,660 -> 1,495 px, and Contact 721 -> 597 px.
- The 2910 x 1494 screenshot-equivalent pass places Projects at 179 CSS px, its intro at 279 px, and the centered card at 393 px. The header ends at 91 px, leaving an intentional 88 px section entrance and only 57 px between intro and card.
- Typography, graphite/bone/cobalt tokens, image sharpness, section order, all 24 project cards, and the 481 px desktop / 444 px mobile centered-card proportions remain intact.
- Coverflow interaction again passed center index 0 -> 1 by Next, 1 -> 2 by wheel, and 2 -> 3 by drag. The centered transform remains `translate3d(0px, 0px, 80px) rotateY(0deg) scale(1.08)`.
- Browser-rendered checks passed at desktop, mobile, and the user's screenshot-equivalent density: HTTP 200, correct title and URL, meaningful content, no framework overlay, no horizontal document overflow, no WebGL error, no page error, and no console warning or error.
- Post-fix combined comparison of the before and after desktop and mobile captures found no remaining P0/P1/P2 spacing, crop, wrapping, or interaction issue. No focused region beyond Projects was necessary because all other section details remained legible in the normalized full-page pair and their numeric spacing bounds were collected directly from the rendered DOM.

### Comparison history, continued

8. The current-run audit identified two blocking mismatches: Ekua showed a different product, and independent section/gap values created excessive and inconsistent whitespace. The first implementation replaced the card with authenticated repository evidence and introduced a shared cadence. Browser QA then found 7-32 px of hidden overflow in the five mobile skill panels after the density reduction. The mobile panel gap and row padding were tightened, all five panels were reopened, and the final pass measured zero overflow. The same pass retained the original 3D project interaction and produced the final matched before/after evidence above.

final result: passed

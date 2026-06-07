from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_required
from flask_login import current_user

from app import db

from app.models.plan import Plan
from app.models.booking import Booking
from app.models.slot import Slot
from app.models.frequency import Frequency


# ====================================
# BLUEPRINT
# ====================================

plans = Blueprint(
    'plans',
    __name__
)


# ====================================
# PLANS PAGE
# ====================================

@plans.route('/plans')
@login_required
def plans_page():
    # Plans page removed — redirect to Tips
    return redirect(url_for('plans.tips_page'))


@plans.route('/tips')
@login_required
def tips_page():

    # Static tips list (1..10) with short preview and full content
    tips = [
        {
            "id": 1,
            "title": "Shade is your paint's best friend",
            "excerpt": "Sunlight is the silent killer of automotive paint. Protect your vehicle from harsh UV rays.",
            "content": """
Continuous exposure to sunlight is one of the biggest threats to your vehicle's paintwork. Ultraviolet (UV) radiation slowly breaks down the clear coat layer that protects automotive paint, causing oxidation, fading, and loss of gloss over time. In Indian weather conditions, where temperatures can remain extremely high for months, this process accelerates significantly.

When paint begins to oxidize, the vehicle develops a dull and chalky appearance. Dark-colored vehicles are particularly vulnerable because they absorb more heat from sunlight. Plastic trims, rubber seals, and headlights are also affected by prolonged UV exposure, often becoming brittle or discolored.

Whenever possible, choose shaded or covered parking areas. Basement parking, covered society parking, or dedicated car sheds provide excellent protection. If covered parking is unavailable, investing in a breathable, high-quality car cover can reduce direct sunlight exposure while preventing dust accumulation.

Regular washing and periodic application of wax or paint sealants further strengthen protection against UV damage. These products create a sacrificial barrier between the paint and environmental contaminants.

Protecting your vehicle from excessive sunlight is one of the simplest and most cost-effective maintenance practices. A few preventive measures today can help preserve paint quality, improve resale value, and keep your car looking newer for many years.
"""
        },
        {
            "id": 2,
            "title": "The Two-Bucket Washing Method",
            "excerpt": "Using two buckets during a car wash dramatically reduces swirl marks and paint scratches.",
            "content": """
Many car owners unknowingly damage their vehicle's paint during routine washing. One of the biggest reasons is using a single bucket for the entire wash process. As dirt, sand, and road grime accumulate in the wash water, they get trapped in the sponge or wash mitt and are repeatedly rubbed across the paint surface. This creates fine scratches known as swirl marks, which gradually dull the vehicle's finish.

The two-bucket washing method is a professional detailing technique designed to minimize this risk. The first bucket contains clean water mixed with car shampoo, while the second bucket contains plain water for rinsing the wash mitt. After cleaning a section of the vehicle, the mitt is rinsed in the plain water bucket to remove trapped dirt before being dipped back into the shampoo bucket.

This simple separation significantly reduces the amount of abrasive particles that come into contact with the paint. Over time, it helps preserve the vehicle's gloss and reduces the need for costly paint correction treatments.

For even better results, use grit guards at the bottom of both buckets. These devices trap dirt beneath the guard and prevent it from being picked up again during washing.

The two-bucket method is especially important for dark-colored vehicles where scratches and swirl marks are more visible. Combined with quality microfiber wash mitts and proper drying techniques, it provides a safer and more professional cleaning process.

A few extra minutes spent using two buckets can save years of unnecessary paint damage and help maintain a showroom-quality appearance.
"""
        },
        {
            "id": 3,
            "title": "Microfiber Over Everything Else",
            "excerpt": "High-quality microfiber materials help protect your vehicle's surfaces while delivering superior cleaning results.",
            "content": """
Many vehicle owners focus heavily on shampoos, waxes, and cleaning chemicals but overlook one of the most important elements of car care: the cloth used during cleaning. A poor-quality cloth can cause more damage than the dirt being removed. This is why professional detailers rely heavily on microfiber towels for almost every cleaning task.

Microfiber is made from extremely fine synthetic fibers that are much smaller than human hair. These fibers create a large surface area capable of trapping dust, dirt, and moisture deep within the cloth rather than dragging contaminants across the vehicle's surface. This significantly reduces the risk of scratches, swirl marks, and paint defects.

Traditional cotton towels and old rags tend to push dirt around rather than safely lifting it away. Over time, repeated use of such materials can leave visible marks on paintwork, glass, and interior surfaces. Microfiber, on the other hand, is soft, highly absorbent, and designed specifically for delicate automotive finishes.

Different microfiber towels can be used for different tasks. Plush towels work well for drying and buffing, while tighter-weave towels are excellent for cleaning glass without leaving lint behind. Interior detailing also becomes easier because microfiber effectively captures dust from dashboards, door panels, and touchscreens.

To maintain effectiveness, microfiber towels should be washed separately from regular laundry and should not be exposed to fabric softeners, which can clog the fibers.

Investing in quality microfiber products is one of the most cost-effective upgrades any car owner can make. Proper microfiber care not only improves cleaning performance but also helps preserve your vehicle's appearance for years.
"""
        },
        {
            "id": 4,
            "title": "Bird Droppings: The 5-Minute Rule",
            "excerpt": "Bird droppings are highly acidic; remove them quickly to avoid permanent paint damage.",
            "content": """
One of the most underestimated threats to a vehicle's exterior is bird droppings. While they may appear to be a minor inconvenience, bird droppings contain highly acidic compounds that can begin damaging automotive paint within a surprisingly short period of time. During hot weather, the damage can occur even faster because heat accelerates the chemical reaction between the contaminants and the paint surface.

Modern automotive paint consists of multiple layers, including a protective clear coat. When bird droppings remain on the surface for extended periods, the acids start to break down this protective layer. The result is often visible staining, dull spots, or permanent etching that cannot be removed through normal washing.

This is why professional detailers recommend following the "5-Minute Rule." The idea is simple: remove bird droppings as soon as reasonably possible instead of waiting for the next scheduled wash. Even a quick cleaning can significantly reduce the risk of damage.

Keep a microfiber cloth and a small detailing spray inside your vehicle for emergencies. Never scrub dry droppings directly from the paint, as hardened particles can create scratches. Instead, spray the affected area, allow the contamination to soften, and gently wipe it away.

The same principle applies to tree sap, insect remains, and other organic contaminants. These substances can also damage paint if ignored for long periods.

Developing the habit of inspecting your vehicle regularly and addressing contaminants immediately helps preserve paint quality, maintain shine, and protect resale value. A few minutes of attention today can prevent expensive paint correction work tomorrow.
"""
        },
        {
            "id": 5,
            "title": "Why Regular Tyre Care Matters",
            "excerpt": "Tyres affect safety, appearance, fuel efficiency, and overall vehicle performance.",
            "content": """
Many vehicle owners focus heavily on paint, interiors, and engine maintenance while neglecting tyre care. However, tyres play a critical role in vehicle safety and driving performance. They are responsible for maintaining grip, supporting vehicle weight, absorbing road shocks, and enabling effective braking. Poor tyre maintenance not only affects appearance but can also increase the risk of accidents.

Over time, tyres accumulate dust, mud, oil, brake residue, and road chemicals. These contaminants can gradually dry out the rubber, causing premature aging and cracking. Continuous exposure to sunlight and high temperatures further accelerates this process. Regular cleaning helps remove harmful contaminants and keeps the rubber in better condition.

Maintaining proper tyre pressure is equally important. Underinflated tyres increase rolling resistance, causing higher fuel consumption and uneven wear. Overinflated tyres reduce road contact, affecting handling and braking performance. Checking tyre pressure at least once every two weeks helps improve both safety and efficiency.

Tyre dressing products can also be beneficial when used correctly. Quality water-based tyre dressings restore a clean, dark appearance while providing additional UV protection. However, excessive use of low-quality products may attract more dust and dirt.

Drivers should also inspect tyres regularly for cuts, punctures, sidewall damage, or uneven tread wear. Early detection often prevents larger and more expensive problems later.

A clean and well-maintained tyre not only improves vehicle appearance but also contributes directly to safer driving. Regular tyre care is a small investment of time that delivers long-term benefits in safety, performance, fuel economy, and overall vehicle longevity.
"""
        },
        {
            "id": 6,
            "title": "Keep Your Car Interior Dust-Free",
            "excerpt": "Regular interior care improves comfort, hygiene, and long-term value.",
            "content": """
Many car owners focus primarily on washing the exterior while overlooking the interior. However, the cabin is the environment you interact with every day, making interior cleanliness just as important as exterior appearance. Dust, dirt, food particles, moisture, and pollutants gradually accumulate inside the vehicle and can affect both comfort and hygiene.

Dust may seem harmless, but over time it settles into air vents, dashboards, seats, carpets, and electronic controls. When the air conditioning system operates, these particles can circulate throughout the cabin, reducing air quality and creating an uncomfortable environment. This becomes especially important for families with children, elderly passengers, or individuals with allergies.

Regular vacuuming helps remove hidden dirt from carpets, floor mats, and seat crevices. Dashboard surfaces should be cleaned using soft microfiber cloths to prevent scratches. Interior plastics and vinyl materials benefit from periodic cleaning and UV protection products, which help prevent fading, cracking, and discoloration caused by sunlight exposure.

Special attention should be given to high-touch areas such as steering wheels, gear knobs, door handles, touchscreens, and buttons. These surfaces often accumulate oils, fingerprints, and bacteria through daily use.

Keeping the interior clean also helps preserve vehicle value. Buyers often judge a vehicle's condition based on the cleanliness of the cabin. A well-maintained interior creates a strong impression that the vehicle has been cared for properly.

Developing a simple weekly interior cleaning routine can significantly improve comfort, appearance, and overall driving experience. A clean cabin not only feels better but also contributes to a healthier and more enjoyable journey every time you get behind the wheel.
"""
        },
        {
            "id": 7,
            "title": "Never Wash Your Car Under Direct Sunlight",
            "excerpt": "High heat causes rapid evaporation and water spots; wash in shade or cooler hours.",
            "content": """
Many vehicle owners prefer washing their cars during the middle of the day because of better visibility and convenience. However, direct sunlight is one of the worst conditions for washing a vehicle. High temperatures cause water, shampoo, and cleaning solutions to evaporate much faster than intended, often before they can be properly rinsed away.

When water evaporates rapidly, it leaves behind mineral deposits and contaminants that create water spots on paint, glass, and chrome surfaces. These spots can become difficult to remove and may require additional polishing or detailing work. Dark-colored vehicles are particularly vulnerable because they absorb more heat, increasing surface temperatures significantly.

Sunlight also affects the performance of car shampoo and cleaning chemicals. Most automotive cleaning products are designed to remain on the surface for a specific period to loosen dirt and contaminants. Under intense heat, these products may dry prematurely, reducing their effectiveness and increasing the risk of streaks.

Another issue is that hot paint surfaces become more sensitive during cleaning. Wiping or scrubbing a heated panel can increase the likelihood of swirl marks and micro-scratches, especially if dirt particles remain on the surface.

For best results, wash your vehicle during the early morning or late evening when temperatures are lower. If possible, choose a shaded area such as a covered parking space or garage. This allows cleaning products to work properly and provides more time for careful rinsing and drying.

By simply avoiding direct sunlight during washing, you can achieve a cleaner finish, reduce water spots, protect the paint, and maintain a more professional-looking appearance for your vehicle.
"""
        },
        {
            "id": 8,
            "title": "The Importance of Clean and Clear Windows",
            "excerpt": "Clean windows improve visibility and safety; maintain both interior and exterior glass.",
            "content": """
Many drivers underestimate the importance of keeping vehicle windows clean. While dirty windows may seem like a minor cosmetic issue, they can significantly affect visibility and driving safety. Dust, fingerprints, water spots, pollution residue, and oily films gradually build up on glass surfaces, reducing clarity and increasing glare.

During daytime driving, dirt on the windshield can scatter sunlight and make it harder to see road signs, pedestrians, and other vehicles. At night, the problem becomes even more serious. Headlights from oncoming vehicles create glare when light passes through dirty glass, making it difficult for drivers to judge distance and react quickly.

The inside surface of the windshield is often overlooked. Over time, air-conditioning systems, interior plastics, and everyday use create a thin film on the glass that may not be immediately visible. This film contributes to fogging and reduced visibility, especially during rainy weather or temperature changes.

Regular cleaning of all glass surfaces—including the windshield, side windows, rear windshield, mirrors, and sunroof—helps maintain clear visibility. Using dedicated automotive glass cleaners and clean microfiber towels ensures streak-free results without scratching the surface.

Drivers should also inspect windshield wipers regularly. Worn-out wipers can leave streaks and reduce effectiveness during rain. Replacing damaged blades at the right time improves safety and prevents unnecessary stress while driving.

Clean windows contribute to a safer driving experience, better visibility, and a more premium appearance. Spending a few minutes maintaining your vehicle's glass can greatly improve both comfort and confidence on the road, regardless of weather conditions.
"""
        },
        {
            "id": 9,
            "title": "Protect Your Vehicle with Regular Waxing",
            "excerpt": "Waxing enhances shine, creates a protective barrier, and preserves paint over time.",
            "content": """
A vehicle's paint is constantly exposed to environmental contaminants such as dust, pollution, bird droppings, tree sap, road grime, and harmful ultraviolet (UV) rays from the sun. Over time, these elements slowly degrade the paint surface, reducing gloss and causing premature aging. One of the simplest and most effective methods to protect automotive paint is regular waxing.

Car wax acts as a protective layer that sits on top of the paint's clear coat. Instead of contaminants directly affecting the paint surface, they interact with the wax layer first. This additional barrier helps reduce oxidation, fading, staining, and environmental damage.

Another major benefit of waxing is improved water repellency. When water lands on a properly waxed vehicle, it forms beads and rolls off more easily, carrying dust and dirt away with it. This makes routine cleaning easier and reduces the chance of water spots forming on the paint.

Regular waxing also enhances the vehicle's appearance by increasing depth, gloss, and color richness. Dark-colored vehicles especially benefit from waxing because it produces a deeper and more reflective finish.

For most vehicles, applying wax every two to three months provides sufficient protection. However, cars frequently exposed to harsh weather conditions may require more frequent applications. Before waxing, always ensure the vehicle is properly washed and dried to avoid trapping dirt beneath the protective layer.

A consistent waxing schedule not only keeps your vehicle looking showroom fresh but also helps maintain resale value. Protecting paint today can prevent costly paint correction or refinishing work in the future, making waxing a smart long-term investment.
"""
        },
        {
            "id": 10,
            "title": "Consistency Beats Occasional Deep Cleaning",
            "excerpt": "Regular maintenance is more effective and economical than occasional intensive cleaning.",
            "content": """
One of the biggest mistakes vehicle owners make is treating car care as an occasional activity rather than a regular habit. A vehicle that is cleaned consistently will almost always remain in better condition than one that receives intensive cleaning only a few times each year. Regular maintenance prevents dirt, contaminants, and environmental damage from accumulating to harmful levels.

Dust, mud, bird droppings, tree sap, road grime, and pollution begin affecting your vehicle the moment it is exposed to the environment. When these contaminants remain on the surface for extended periods, they become harder to remove and may permanently damage paint, glass, rubber trims, and other components. Regular cleaning prevents these problems before they develop.

Consistent maintenance also allows owners to identify minor issues early. Small scratches, tyre wear, damaged wipers, paint defects, or fluid leaks are easier and less expensive to address when detected quickly. Waiting until a major problem appears often results in significantly higher repair costs.

The same principle applies to vehicle interiors. Weekly dust removal and periodic vacuuming prevent dirt from becoming deeply embedded in carpets, seats, and interior surfaces. This helps maintain comfort, hygiene, and long-term appearance.

For best results, create a simple maintenance schedule. This may include weekly exterior washing, interior dusting, tyre inspections, monthly glass treatment, and periodic paint protection. Such routines require very little time but deliver substantial long-term benefits.

Professional vehicle care is not about perfection; it is about consistency. Small efforts performed regularly protect your investment, improve driving satisfaction, maintain resale value, and ensure your vehicle remains clean, attractive, and well-maintained throughout its life.
"""
        }
    ]

    return render_template(
        'tips/tips.html',
        tips=tips,
        user=current_user
    )


# ====================================
# SCHEDULE PAGE
# ====================================

@plans.route(
    '/plans-schedule',
    methods=['GET', 'POST']
)
@login_required
def schedule():

    # ====================================
    # LOAD DATA
    # ====================================

    frequencies = Frequency.query.filter_by(
        is_active=True
    ).all()

    plans_data = Plan.query.filter_by(
        is_active=True
    ).all()

    slots = Slot.query.filter_by(
        is_active=True
    ).all()


    # ====================================
    # BOOKING SUBMIT
    # ====================================

    if request.method == 'POST':

        frequency_id = request.form.get(
            'frequency_id'
        )

        plan_id = request.form.get(
            'plan_id'
        )

        slot_id = request.form.get(
            'slot_id'
        )


        # ====================================
        # VALIDATION
        # ====================================

        if not frequency_id:

            flash('Please Select Frequency')

            return redirect(
                url_for('plans.schedule')
            )

        if not plan_id:

            flash('Please Select Service Tier')

            return redirect(
                url_for('plans.schedule')
            )

        if not slot_id:

            flash('Please Select Time Slot')

            return redirect(
                url_for('plans.schedule')
            )


        # ====================================
        # FETCH OBJECTS
        # ====================================

        selected_frequency = Frequency.query.get(
            int(frequency_id)
        )

        selected_plan = Plan.query.get(
            int(plan_id)
        )

        selected_slot = Slot.query.get(
            int(slot_id)
        )


        # ====================================
        # SLOT FULL CHECK
        # ====================================

        if selected_slot.is_full:

            flash('Selected Slot Is Full')

            return redirect(
                url_for('plans.schedule')
            )


        # ====================================
        # DELETE OLD PENDING BOOKING
        # ====================================

        old_booking = Booking.query.filter_by(

            user_id=current_user.id,
            payment_status='Pending'

        ).first()

        if old_booking:

            db.session.delete(old_booking)

            db.session.commit()


        # ====================================
        # CREATE BOOKING
        # ====================================

        booking = Booking(

            user_id=current_user.id,

            frequency_name=selected_frequency.name,

            plan_name=selected_plan.name,

            slot_time=selected_slot.slot_time,

            slot_shift=selected_slot.shift,

            plan_price=selected_plan.price,

            booking_status='Confirmed',

            payment_status='Pending',

            service_status='Scheduled'
        )

        db.session.add(booking)


        # ====================================
        # UPDATE SLOT
        # ====================================

        selected_slot.current_bookings += 1

        selected_slot.update_slot_status()


        # ====================================
        # UPDATE USER ACTIVE PLAN
        # ====================================

        current_user.active_plan = (
            selected_plan.name
        )


        # ====================================
        # SAVE
        # ====================================

        db.session.commit()


        flash(
    'Booking Confirmed Successfully'
)

        return redirect(
    url_for(
        'payment.payment_page',
        
    )
)


    # ====================================
    # PAGE LOAD
    # ====================================

    return render_template(

        'plans/schedule.html',

        frequencies=frequencies,

        plans=plans_data,

        slots=slots,

        user=current_user
    )


# ====================================
# SELECT PLAN
# ====================================

@plans.route('/select-plan/<int:plan_id>')
@login_required
def select_plan(plan_id):

    selected_plan = Plan.query.get_or_404(
        plan_id
    )

    old_booking = Booking.query.filter_by(

        user_id=current_user.id,
        payment_status='Pending'

    ).first()

    if old_booking:

        db.session.delete(old_booking)

        db.session.commit()

    booking = Booking(

        user_id=current_user.id,

        plan_name=selected_plan.name,

        plan_price=selected_plan.price,

        booking_status='Pending',

        payment_status='Pending',

        service_status='Plan Selected'
    )

    current_user.active_plan = (
        selected_plan.name
    )

    db.session.add(booking)

    db.session.commit()

    flash(
        'Plan Selected Successfully'
    )

    return redirect(
    url_for(
        'booking.schedule'
    )
)
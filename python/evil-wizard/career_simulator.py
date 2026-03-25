# ============================================================
# Visible — Career Strategy Simulator
# Advanced Python Module Project: Defeat the Evil Wizard
# Coding Temple Advanced Python Module
#
# The assignment requires a turn-based battle game using OOP.
# This implementation reskins the wizard battle as a career
# strategy simulation. The player is a professional navigating
# an organization. The Evil Wizard is The Corporate Machine —
# forced ranking, budget cuts, and political maneuvering.
#
# OOP concepts demonstrated:
#   - Inheritance: all characters inherit from CareerAgent
#   - Special abilities: two unique moves per archetype
#   - Healing mechanic: sponsor reconnection restores leverage
#   - Randomized damage: contributions have variable impact
#   - Turn-based battle system with menu choices
#   - Victory/defeat messages
#
# Character archetypes (4 required):
#   1. Operator    — process-driven, invisible labor specialist
#   2. Strategist  — long-term builder, revenue connector
#   3. Advocate    — relationship capital, sponsorship network
#   4. Specialist  — deep expertise, external market value
# ============================================================

import random
import time


# ============================================================
# BASE CLASS
# ============================================================

class CareerAgent:
    """
    Base class for all characters in the Career Strategy Simulator.
    Represents a professional navigating organizational power.

    Attributes:
        name (str):           Character name
        leverage (int):       Career leverage — equivalent to health
        influence (int):      Attack power — career influence
        max_leverage (int):   Maximum leverage (cannot exceed this)
        special_used (dict):  Tracks special ability usage
    """

    def __init__(self, name, leverage, influence):
        self.name = name
        self.leverage = leverage
        self.influence = influence
        self.max_leverage = leverage
        self.special_used = {}

    def deploy_contribution(self, opponent):
        """
        Standard attack — deploy a contribution as evidence.
        Damage is randomized to reflect variable organizational impact.
        """
        # Random damage within a range around influence power
        damage = random.randint(
            max(1, self.influence - 10),
            self.influence + 10
        )
        opponent.leverage -= damage
        print(f"\n  {self.name} deploys a contribution against "
              f"{opponent.name}!")
        print(f"  Impact: {damage} leverage points removed.")
        if opponent.leverage <= 0:
            print(f"\n  {opponent.name} has been outmaneuvered!")

    def heal(self):
        """
        Healing mechanic — reconnect with a sponsor or document a win.
        Restores leverage but cannot exceed maximum.
        """
        heal_amount = random.randint(15, 30)
        before = self.leverage
        self.leverage = min(self.leverage + heal_amount, self.max_leverage)
        actual_heal = self.leverage - before
        print(f"\n  {self.name} reconnects with a sponsor and "
              f"documents a win.")
        print(f"  Leverage restored: +{actual_heal} "
              f"(now {self.leverage}/{self.max_leverage})")

    def display_stats(self):
        """Display current leverage and influence stats."""
        bar_length = 20
        filled = int((self.leverage / self.max_leverage) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\n  {self.name}")
        print(f"  Leverage: [{bar}] {self.leverage}/{self.max_leverage}")
        print(f"  Influence: {self.influence}")

    def is_defeated(self):
        """Check if this agent has been outmaneuvered."""
        return self.leverage <= 0


# ============================================================
# PLAYER CHARACTER CLASSES
# ============================================================

class Operator(CareerAgent):
    """
    The Operator — process-driven, invisible labor specialist.
    Excels at documenting operational contributions that others
    overlook. Strength in continuity premium and system ownership.

    Special Abilities:
        1. Continuity Premium  — quantify replacement cost to org
        2. Efficiency Proof    — show time saved, process improved
    """

    def __init__(self, name):
        super().__init__(name, leverage=140, influence=22)
        self.archetype = "Operator"
        self.strength = "Process documentation and continuity value"

    def continuity_premium(self, opponent):
        """
        Special Ability 1: Continuity Premium
        Quantify the replacement cost the organization would face
        if you left. High impact — hard to dismiss.
        Deals bonus damage and reduces opponent's next attack.
        """
        if self.special_used.get('continuity_premium'):
            print("\n  Continuity Premium already deployed this session.")
            return False

        damage = random.randint(35, 50)
        opponent.leverage -= damage
        opponent.influence = max(5, opponent.influence - 8)
        self.special_used['continuity_premium'] = True

        print(f"\n  {self.name} activates CONTINUITY PREMIUM!")
        print(f"  'Replacing me would cost 3x my salary and take")
        print(f"  18 months. Here is the documented evidence.'")
        print(f"  {opponent.name} is destabilized: -{damage} leverage")
        print(f"  {opponent.name}'s influence reduced by 8.")
        return True

    def efficiency_proof(self, opponent):
        """
        Special Ability 2: Efficiency Proof
        Document measurable time saved and process improvements.
        Consistent moderate damage — the steady accumulation
        of operational evidence is hard to argue against.
        """
        if self.special_used.get('efficiency_proof'):
            print("\n  Efficiency Proof already deployed this session.")
            return False

        damage = random.randint(25, 40)
        self_heal = random.randint(10, 20)
        opponent.leverage -= damage
        self.leverage = min(self.leverage + self_heal, self.max_leverage)
        self.special_used['efficiency_proof'] = True

        print(f"\n  {self.name} activates EFFICIENCY PROOF!")
        print(f"  'This process now takes 12 hours instead of 40.")
        print(f"  Here is the before and after documentation.'")
        print(f"  {opponent.name} takes {damage} leverage damage.")
        print(f"  {self.name} gains {self_heal} leverage "
              f"(confidence from documented wins).")
        return True


class Strategist(CareerAgent):
    """
    The Strategist — long-term builder, revenue connector.
    Connects their work directly to business outcomes. Excels
    at the pre-emptive performance audit and strategic debt tracking.

    Special Abilities:
        1. Revenue Connection  — link contributions to P&L impact
        2. Strategic Debt Call — expose long-term value ignored
    """

    def __init__(self, name):
        super().__init__(name, leverage=120, influence=30)
        self.archetype = "Strategist"
        self.strength = "Revenue connection and long-term value framing"

    def revenue_connection(self, opponent):
        """
        Special Ability 1: Revenue Connection
        Connect your contribution directly to revenue impact.
        High damage — organizations cannot ignore direct P&L links.
        """
        if self.special_used.get('revenue_connection'):
            print("\n  Revenue Connection already deployed this session.")
            return False

        damage = random.randint(40, 60)
        opponent.leverage -= damage
        self.special_used['revenue_connection'] = True

        print(f"\n  {self.name} activates REVENUE CONNECTION!")
        print(f"  'This initiative I led contributed $2.4M ARR")
        print(f"  in Q3. Here is the attribution chain.'")
        print(f"  {opponent.name} cannot dismiss the P&L evidence:")
        print(f"  -{damage} leverage damage.")
        return True

    def strategic_debt_call(self, opponent):
        """
        Special Ability 2: Strategic Debt Call
        Name the long-term work that was never recognized.
        Moderate damage with high narrative impact — forces the
        organization to account for contributions ignored at
        the time because they were beyond the review cycle.
        """
        if self.special_used.get('strategic_debt_call'):
            print("\n  Strategic Debt Call already deployed this session.")
            return False

        damage = random.randint(30, 45)
        opponent.leverage -= damage
        self.leverage = min(
            self.leverage + 15, self.max_leverage
        )
        self.special_used['strategic_debt_call'] = True

        print(f"\n  {self.name} activates STRATEGIC DEBT CALL!")
        print(f"  'The 18-month transformation I led did not show")
        print(f"  results in the review cycle. Here is the full")
        print(f"  timeline and the outcomes now visible.'")
        print(f"  {opponent.name} is forced to account for ignored")
        print(f"  contributions: -{damage} leverage.")
        print(f"  {self.name} gains 15 leverage (vindication).")
        return True


class Advocate(CareerAgent):
    """
    The Advocate — relationship capital, sponsorship network.
    Builds invisible infrastructure of support. Excels at
    coalition building and sponsor activation.

    Special Abilities:
        1. Sponsor Activation  — call in relationship capital
        2. Coalition Shield    — collective protection from allies
    """

    def __init__(self, name):
        super().__init__(name, leverage=130, influence=25)
        self.archetype = "Advocate"
        self.strength = "Relationship capital and coalition building"

    def sponsor_activation(self, opponent):
        """
        Special Ability 1: Sponsor Activation
        Activate a sponsor relationship built over time.
        Heals self significantly while damaging opponent —
        having a sponsor in the room changes every calculation.
        """
        if self.special_used.get('sponsor_activation'):
            print("\n  Sponsor Activation already deployed this session.")
            return False

        damage = random.randint(25, 35)
        heal = random.randint(25, 40)
        opponent.leverage -= damage
        self.leverage = min(self.leverage + heal, self.max_leverage)
        self.special_used['sponsor_activation'] = True

        print(f"\n  {self.name} activates SPONSOR ACTIVATION!")
        print(f"  'My sponsor has been watching my work for two")
        print(f"  years. They are now in the room advocating for")
        print(f"  what they have directly observed.'")
        print(f"  {opponent.name} loses {damage} leverage.")
        print(f"  {self.name} gains {heal} leverage "
              f"(sponsor support).")
        return True

    def coalition_shield(self, opponent):
        """
        Special Ability 2: Coalition Shield
        Rally allies who will speak on your behalf.
        Primarily defensive — greatly reduces opponent damage
        next turn while dealing moderate damage now.
        """
        if self.special_used.get('coalition_shield'):
            print("\n  Coalition Shield already deployed this session.")
            return False

        damage = random.randint(20, 35)
        shield = random.randint(20, 30)
        opponent.leverage -= damage
        opponent.influence = max(5, opponent.influence - 10)
        self.leverage = min(self.leverage + shield, self.max_leverage)
        self.special_used['coalition_shield'] = True

        print(f"\n  {self.name} activates COALITION SHIELD!")
        print(f"  'Three senior colleagues have submitted written")
        print(f"  evidence of my contributions. The calibration")
        print(f"  committee cannot ignore collective testimony.'")
        print(f"  {opponent.name} loses {damage} leverage and")
        print(f"  10 influence (weakened by collective pushback).")
        print(f"  {self.name} gains {shield} leverage (protected).")
        return True


class Specialist(CareerAgent):
    """
    The Specialist — deep expertise, external market value.
    Holds knowledge the organization cannot easily replace.
    Excels at external leverage and market value demonstration.

    Special Abilities:
        1. External Offer      — use market data as leverage
        2. Knowledge Monopoly  — demonstrate irreplaceable expertise
    """

    def __init__(self, name):
        super().__init__(name, leverage=110, influence=35)
        self.archetype = "Specialist"
        self.strength = "External market value and deep expertise"

    def external_offer(self, opponent):
        """
        Special Ability 1: External Offer
        Demonstrate your external market value with concrete data.
        Highest single-hit damage — external market data is the
        most powerful leverage tool available to any employee.
        """
        if self.special_used.get('external_offer'):
            print("\n  External Offer already deployed this session.")
            return False

        damage = random.randint(45, 65)
        opponent.leverage -= damage
        self.special_used['external_offer'] = True

        print(f"\n  {self.name} activates EXTERNAL OFFER!")
        print(f"  'I have received an offer from a competitor at")
        print(f"  35% above my current compensation. I am sharing")
        print(f"  this because I prefer to stay — but I need you")
        print(f"  to understand my market value.'")
        print(f"  {opponent.name} is severely destabilized:")
        print(f"  -{damage} leverage damage.")
        return True

    def knowledge_monopoly(self, opponent):
        """
        Special Ability 2: Knowledge Monopoly
        Demonstrate knowledge the organization cannot access
        anywhere else. Consistent damage — irreplaceable
        expertise is permanent leverage.
        """
        if self.special_used.get('knowledge_monopoly'):
            print("\n  Knowledge Monopoly already deployed this session.")
            return False

        damage = random.randint(30, 45)
        opponent.leverage -= damage
        opponent.influence = max(5, opponent.influence - 12)
        self.special_used['knowledge_monopoly'] = True

        print(f"\n  {self.name} activates KNOWLEDGE MONOPOLY!")
        print(f"  'I am the only person in this organization who")
        print(f"  understands this system fully. The replacement")
        print(f"  timeline would be 18-24 months minimum.'")
        print(f"  {opponent.name} loses {damage} leverage and")
        print(f"  12 influence (cannot operate without this")
        print(f"  knowledge).")
        return True


# ============================================================
# THE CORPORATE MACHINE — VILLAIN CLASS
# ============================================================

class CorporateMachine(CareerAgent):
    """
    The Corporate Machine — the antagonist.
    Represents the organizational forces that work against
    individual career advancement: forced ranking, budget cuts,
    political maneuvering, and the Welchian variable cost logic.

    Special mechanic:
        regenerate() — the machine recovers after each player turn,
        representing how organizational pressure never fully stops.
    """

    def __init__(self, name="The Corporate Machine"):
        super().__init__(name, leverage=200, influence=18)
        self.regeneration = 8  # Leverage restored each turn
        self.turn_count = 0

    def regenerate(self):
        """
        The machine regenerates each turn.
        Represents the relentless nature of organizational pressure —
        it never fully stops, it just gets managed.
        """
        regen = random.randint(3, self.regeneration)
        self.leverage = min(self.leverage + regen, self.max_leverage)
        print(f"\n  {self.name} regenerates {regen} leverage.")
        print(f"  (Organizational pressure never fully stops.)")

    def attack(self, player):
        """
        The machine attacks with escalating tactics.
        Early turns: performance management pressure.
        Mid turns: forced ranking and budget cuts.
        Late turns: managed out scenario.
        """
        self.turn_count += 1
        damage = random.randint(
            max(1, self.influence - 5),
            self.influence + 8
        )

        # Escalating attack messages based on turn count
        if self.turn_count <= 3:
            tactic = random.choice([
                "performance improvement plan",
                "goal post movement",
                "credit reassignment",
                "scope reduction"
            ])
        elif self.turn_count <= 6:
            tactic = random.choice([
                "forced ranking pressure",
                "budget cut justification",
                "headcount reduction signal",
                "reorg announcement"
            ])
        else:
            tactic = random.choice([
                "managed out scenario",
                "role elimination",
                "succession planning bypass",
                "package offer"
            ])

        player.leverage -= damage
        print(f"\n  {self.name} deploys: {tactic.upper()}!")
        print(f"  {player.name} loses {damage} leverage.")


# ============================================================
# CHARACTER CREATION
# ============================================================

def create_character():
    """
    Guide the player through career archetype selection.
    Returns a player character instance.
    """
    print("\n" + "=" * 55)
    print("  VISIBLE: CAREER STRATEGY SIMULATOR")
    print("=" * 55)
    print("\n  You are facing The Corporate Machine.")
    print("  Choose your career archetype:\n")
    print("  1. OPERATOR")
    print("     Process-driven. Invisible labor specialist.")
    print("     High leverage. Steady damage. Continuity value.")
    print()
    print("  2. STRATEGIST")
    print("     Long-term builder. Revenue connector.")
    print("     Medium leverage. High damage. P&L impact.")
    print()
    print("  3. ADVOCATE")
    print("     Relationship capital. Sponsorship network.")
    print("     Medium-high leverage. Heals well. Coalition power.")
    print()
    print("  4. SPECIALIST")
    print("     Deep expertise. External market value.")
    print("     Lower leverage. Highest damage. Market leverage.")
    print()

    while True:
        choice = input("  Enter 1, 2, 3, or 4: ").strip()
        if choice in ['1', '2', '3', '4']:
            break
        print("  Please enter 1, 2, 3, or 4.")

    name = input("\n  Enter your character's name: ").strip()
    if not name:
        name = "The Professional"

    if choice == '1':
        player = Operator(name)
    elif choice == '2':
        player = Strategist(name)
    elif choice == '3':
        player = Advocate(name)
    else:
        player = Specialist(name)

    print(f"\n  You are {player.name}, the {player.archetype}.")
    print(f"  Strength: {player.strength}")
    print(f"  Leverage: {player.leverage} | Influence: {player.influence}")
    input("\n  Press Enter to begin the battle...")
    return player


# ============================================================
# SPECIAL ABILITY MENU
# ============================================================

def use_special_ability(player, machine):
    """
    Display and execute special ability choices.
    Each archetype has two unique abilities.
    """
    print(f"\n  Choose your special ability:")

    # Define abilities per archetype
    abilities = {
        'Operator': [
            ('1', 'Continuity Premium',
             'Quantify replacement cost. Bonus damage + reduce opponent influence.',
             'continuity_premium'),
            ('2', 'Efficiency Proof',
             'Show time saved. Damage + self heal.',
             'efficiency_proof'),
        ],
        'Strategist': [
            ('1', 'Revenue Connection',
             'Link contributions to P&L. High damage.',
             'revenue_connection'),
            ('2', 'Strategic Debt Call',
             'Expose ignored long-term work. Damage + self heal.',
             'strategic_debt_call'),
        ],
        'Advocate': [
            ('1', 'Sponsor Activation',
             'Call in relationship capital. Damage + strong self heal.',
             'sponsor_activation'),
            ('2', 'Coalition Shield',
             'Rally allies. Damage + reduce opponent + self heal.',
             'coalition_shield'),
        ],
        'Specialist': [
            ('1', 'External Offer',
             'Deploy market value data. Highest single damage.',
             'external_offer'),
            ('2', 'Knowledge Monopoly',
             'Demonstrate irreplaceable expertise. Damage + reduce opponent.',
             'knowledge_monopoly'),
        ],
    }

    archetype_abilities = abilities.get(player.archetype, [])

    for num, name, description, key in archetype_abilities:
        used = player.special_used.get(key, False)
        status = " [DEPLOYED]" if used else ""
        print(f"  {num}. {name}{status}")
        print(f"     {description}")

    print("  3. Back to main menu")

    while True:
        choice = input("\n  Choose ability (1, 2, or 3): ").strip()
        if choice == '3':
            return False
        if choice == '1':
            ability_key = archetype_abilities[0][3]
            ability_method = getattr(
                player, archetype_abilities[0][3], None
            )
            if ability_method:
                return ability_method(machine)
        elif choice == '2':
            ability_method = getattr(
                player, archetype_abilities[1][3], None
            )
            if ability_method:
                return ability_method(machine)
        print("  Please enter 1, 2, or 3.")


# ============================================================
# BATTLE SYSTEM
# ============================================================

def battle(player, machine):
    """
    Main turn-based battle loop.
    Player chooses actions each turn.
    Machine regenerates and attacks after each player turn.
    """
    print("\n" + "=" * 55)
    print(f"  {player.name} vs {machine.name}")
    print("=" * 55)
    print("\n  The Corporate Machine has initiated a performance")
    print("  review cycle. Your leverage is on the line.")
    print("  Deploy your career evidence to survive and advance.")

    turn = 0

    while machine.leverage > 0 and player.leverage > 0:
        turn += 1
        print(f"\n{'─' * 55}")
        print(f"  TURN {turn}")
        print(f"{'─' * 55}")

        # Display quick status
        print(f"\n  YOUR LEVERAGE:    {player.leverage}/{player.max_leverage}")
        print(f"  MACHINE LEVERAGE: {machine.leverage}/{machine.max_leverage}")

        print("\n  YOUR TURN — Choose your action:")
        print("  1. Deploy Contribution  (standard attack)")
        print("  2. Use Special Ability  (unique career move)")
        print("  3. Reconnect with Sponsor (heal)")
        print("  4. View Full Stats")

        while True:
            choice = input("\n  Choose action (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                break
            print("  Please enter 1, 2, 3, or 4.")

        if choice == '1':
            player.deploy_contribution(machine)

        elif choice == '2':
            result = use_special_ability(player, machine)
            if not result:
                # Went back to menu — let player choose again
                player.deploy_contribution(machine)

        elif choice == '3':
            player.heal()

        elif choice == '4':
            player.display_stats()
            machine.display_stats()
            continue  # Don't end turn on stats view

        # Check if machine is defeated
        if machine.leverage <= 0:
            break

        # Machine's turn: regenerate then attack
        print(f"\n{'─' * 55}")
        print(f"  {machine.name.upper()}'S TURN")
        print(f"{'─' * 55}")
        machine.regenerate()
        machine.attack(player)

        # Check if player is defeated
        if player.leverage <= 0:
            break

    # Battle conclusion
    print(f"\n{'=' * 55}")
    if machine.leverage <= 0:
        victory(player)
    else:
        defeat(player)


# ============================================================
# VICTORY AND DEFEAT
# ============================================================

def victory(player):
    """Display victory message with career outcome."""
    print(f"\n  ★ CAREER ADVANCEMENT ACHIEVED ★")
    print(f"{'=' * 55}")
    print(f"\n  {player.name} has outmaneuvered The Corporate Machine.")
    print(f"\n  The calibration committee reviewed the evidence.")
    print(f"  The contribution record was undeniable.")
    print(f"  The promotion conversation is scheduled.")
    print()

    if player.archetype == 'Operator':
        print("  Your continuity premium made the cost of not")
        print("  promoting you clearer than the cost of promoting you.")
    elif player.archetype == 'Strategist':
        print("  Your revenue connection made the ROI of your")
        print("  advancement impossible to argue against.")
    elif player.archetype == 'Advocate':
        print("  Your sponsor network ensured the right people")
        print("  were in the room telling the right story.")
    elif player.archetype == 'Specialist':
        print("  Your external market data forced the organization")
        print("  to price your expertise at its actual market value.")

    print()
    print("  Know your leverage before the meeting.")
    print(f"\n  Final leverage: {player.leverage}/{player.max_leverage}")
    print(f"{'=' * 55}")


def defeat(player):
    """Display defeat message with career guidance."""
    print(f"\n  ✗ MANAGED OUT")
    print(f"{'=' * 55}")
    print(f"\n  {player.name} was outmaneuvered by The Corporate Machine.")
    print()
    print("  The evidence was not strong enough.")
    print("  The timing was not right.")
    print("  Or the environment was not one that could see you.")
    print()
    print("  This is not the end. It is information.")
    print()
    print("  Three questions for your next move:")
    print("  1. Were your contributions documented and attributed?")
    print("  2. Was your environment scoring fairly?")
    print("  3. Did you have the right sponsor in the room?")
    print()
    print("  Visible helps you answer all three before")
    print("  the next battle begins.")
    print(f"\n  Final leverage: {player.leverage}/{player.max_leverage}")
    print(f"{'=' * 55}")


# ============================================================
# MAIN
# ============================================================

def main():
    """
    Main entry point. Creates character and initiates battle.
    """
    player = create_character()
    machine = CorporateMachine()
    battle(player, machine)

    # Play again option
    print()
    again = input("  Play again? (y/n): ").strip().lower()
    if again == 'y':
        main()
    else:
        print("\n  Build your evidence. Know your leverage.")
        print("  Visible — career decision intelligence.\n")


if __name__ == "__main__":
    main()

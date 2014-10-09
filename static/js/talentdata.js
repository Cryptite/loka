var data = [
    // offensive
    [
        {
            index: 1,
            name: "Hot Bow",
            ranks: 1,
            desc: "Arrows have a 15% chance to set their target on fire.\n\nPassive Effect",
            rankInfo: []
        },
        {
            index: 2,
            name: "Flaming Sword",
            ranks: 1,
            desc: "All sword attacks have a 15% chance to ignite the enemy, dealing fire damage over time.\nPassive Effect",
            rankInfo: []
        },
        {
            index: 3,
            name: "Archer",
            ranks: 1,
            desc: "Battleground bow is granted Power II\n\nPassive Effect",
            rankInfo: []
        },
        {
            index: 4,
            name: "Slow",
            ranks: 1,
            desc: "Sword attacks have a 15% chance to slow enemies\nPassive Effect",
            rankInfo: []
        },
        {
            index: 5,
            name: "Groove",
            ranks: 1,
            desc: "Every time you land a hit with an arrow on an enemy, you gain +10% damage on arrow shots up to 30%. Each miss reduces Groove by 10%\n\nPassive Ability",
            rankInfo: []
        },
        {
            index: 6,
            name: "Life Steal",
            ranks: 1,
            desc: "Upon hitting an enemy, you gain Lifesteal.\nLifesteal: You regain a small amount of health every second for 6 seconds. This can only occur once every 30 seconds.\nPassive Effect\nCooldown: 30 seconds",
            rankInfo: []
        },
        {
            index: 7,
            name: "Frost Trap",
            ranks: 1,
            desc: "Place a trap that, when run over by an enemy, applies a heavy slow and minor poison to the enemy.\n\nCooldown: 30 seconds\n\nAbility",
            parent: 0,
            rankInfo: []
        },
        {
            index: 8,
            name: "Thrill of the Kill",
            ranks: 1,
            desc: "Sword damage increased by 15%. Additionally, any time you kill a player, you gain Speed III for 6 seconds.\nRequires Life Steal\nPassive Effect",
            parent: 3,
            rankInfo: []
        },
        {
            index: 9,
            name: "Explosive Arrow",
            ranks: 1,
            desc: "Loads an Explosive Arrow that devastates nearby enemies upon impact.\nA Player hit directly by the shot will take double damage.\nCooldown: 25 seconds.\nAbility",
            rankInfo: []
        },
        {
            index: 10,
            name: "Lunge",
            ranks: 1,
            desc: "Leap forward toward your enemy. Your next attack within 8 seconds does twice the usual damage.\nCooldown: 20 seconds\nAbility",
            rankInfo: []
        }
    ],
    // defensive
    [
        {
            index: 1,
            name: "Summoner's Resolve",
            ranks: 1,
            desc: "Improves the following Summoner Spells:\n\n|Cleanse:| Increases duration of disable reduction by 1 second\n|Heal:| Passively increases Health by 5 per level\n|Smite:| Grants 10 bonus gold on use\n|Barrier:| Increases Barrier shield amount by 20",
            rankInfo: []
        },
        {
            index: 2,
            name: "Perseverance",
            ranks: 3,
            desc: "Grants up to +# Health Regen per 5 seconds based on missing Health",
            rankInfo: [2, 4, 6]
        },
        {
            index: 3,
            name: "Durability",
            ranks: 4,
            perlevel: 1,
            desc: "+# Health per level\n(+# Health at champion level 18)",
            rankInfo: [1.5, 3, 4.5, 6]
        },
        {
            index: 4,
            name: "Tough Skin",
            ranks: 2,
            desc: "Reduces damage taken from monsters by #",
            rankInfo: [1, 2]
        },
    ],
    [
        {
            index: 1,
            name: "Summoner's Insight",
            ranks: 1,
            desc: "Improves the following Summoner Spells:\n\n|Teleport:| Reduces cast time by # second\n|Revive:| Grants bonus Health on Revive for 2 minutes\n|Flash:| Reduces cooldown by 15 seconds\n|Clarity:| Increases Mana restored by 25%\n|Clairvoyance:| Grants additional vision of enemy units revealed",
            rankInfo: [0.5]
        },
        {
            index: 2,
            name: "Wanderer",
            ranks: 3,
            desc: "Grants +#% increased Movement Speed when out of combat",
            rankInfo: [0.66, 1.33, 2]
        },
        {
            index: 3,
            name: "Meditation",
            ranks: 3,
            desc: "+# Mana Regen per 5 seconds",
            rankInfo: [1, 2, 3]
        },
        {
            index: 4,
            name: "Improved Recall",
            ranks: 1,
            desc: "Reduces the cast time of Recall by 1 second and Enhanced Recall by # seconds",
            rankInfo: [0.5]
        },
    ]
];

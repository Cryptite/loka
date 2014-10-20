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
            parent: 4,
            rankInfo: []
        },
        {
            index: 8,
            name: "Thrill of the Kill",
            ranks: 1,
            desc: "Sword damage increased by 15%. Additionally, any time you kill a player, you gain Speed III for 6 seconds.\nRequires Life Steal\nPassive Effect",
            parent: 5,
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
            name: "Stand Your Ground",
            ranks: 1,
            desc: "Grants Blast Protection, reducing knockback and damage from explosions.\nEquipment Upgrade",
            rankInfo: []
        },
        {
            index: 2,
            name: "Reflexes",
            ranks: 1,
            desc: "For 3 seconds you block all arrows that hit you.\nTo use: Block with your sword\nCooldown: 15 seconds\nAbility",
            rankInfo: []
        },
        {
            index: 3,
            name: "Fresh Start",
            ranks: 1,
            desc: "Grants Absorption I",
            rankInfo: []
        },
        {
            index: 4,
            name: "Flame Retardant",
            ranks: 2,
            desc: "Grants Fire Protection, reducing time spent burning.\nEquipment Upgrade",
            rankInfo: []
        },
        {
            index: 5,
            name: "Pointy",
            ranks: 1,
            desc: "Grants Thorns II",
            rankInfo: []
        },
        {
            index: 6,
            name: "Iron Form",
            ranks: 1,
            desc: "Incoming damage has a chance to trigger Iron Form\nIron Form:Grants Resistance, lowering damage taken for 7 seconds.\nThis can only occur once every 30 seconds.\nPassive Effect",
            rankInfo: []
        },
        {
            index: 7,
            name: "Resolve",
            ranks: 1,
            desc: "Move 50% faster for 4 seconds and take no knockback when hit in combat.\nCooldown: 20 seconds\nAbility",
            rankInfo: []
        },
        {
            index: 8,
            name: "Hardened",
            ranks: 1,
            desc: "Your armor is more effective.\nEquipment Upgrade",
            rankInfo: []
        },
        {
            index: 9,
            name: "Quake",
            ranks: 1,
            desc: "Knocks all nearby enemies several blocks into the air and then roots them for several seconds.\nCooldown: 30 seconds\nAbility",
            rankInfo: []
        },
        {
            index: 10,
            name: "Last Stand",
            ranks: 1,
            desc: "Take no physical damage for 5 seconds. Damage potions will still harm you.\nCooldown: 45 seconds\nAbility",
            parent: 7,
            rankInfo: []
        }
    ],
    [
        {
            index: 1,
            name: "Fleet Footed",
            ranks: 1,
            desc: "Grants Speed I",
            rankInfo: []
        },
        {
            index: 2,
            name: "Bandage",
            ranks: 1,
            desc: "Grants a bandage, heals you if not moving.",
            rankInfo: []
        },
        {
            index: 3,
            name: "Bouncy",
            ranks: 1,
            desc: "Grants Feather Falling I and Jump I",
            rankInfo: []
        },
        {
            index: 4,
            name: "Potency",
            ranks: 1,
            desc: "You are awarded an additional Splash Potion of Healing.\nEquipment Upgrade",
            rankInfo: []
        },
        {
            index: 5,
            name: "Potion Slinger",
            ranks: 1,
            desc: "You are granted 1 additional Splash Potion of Harming and can throw all potions twice as far.\nEquipment Upgrade",
            rankInfo: []
        },
        {
            index: 6,
            name: "Holy Grenade",
            ranks: 1,
            parent: 3,
            desc: "Your healing potions affect a wider range, better healing friendlies, and no longer heal enemies.",
            rankInfo: []
        },
        {
            index: 7,
            name: "Rallying Cry",
            ranks: 1,
            desc: "Cry out, granting an extra Harming Potion, 15% extra damage, and Speed II to all nearby friendlies for 7 seconds.\nAlso drops a beacon on the ground that friendlies can run over to get a Speed buff.\nCooldown: 45 seconds\nAbility",
            rankInfo: []
        },
        {
            index: 8,
            name: "Life Shield",
            ranks: 1,
            desc: "You and all nearby friendlies are granted Absorption III for 8 seconds.\nCooldown: 35 seconds\nAbility",
            rankInfo: []
        },
        {
            index: 9,
            name: "Aura of Silence",
            ranks: 1,
            desc: "Gives some sort of aura and silences nearby enemies when cast.",
            rankInfo: []
        },
        {
            index: 10,
            name: "Freyjia's Arrow",
            ranks: 1,
            desc: "Loads Freyjia's Arrow. Wherever your arrow lands grants a 6 seconds of regeneration to nearby friendlies and weakens nearby enemies.\nCooldown: 45 seconds\nAbility",
            rankInfo: []
        },
    ]
];

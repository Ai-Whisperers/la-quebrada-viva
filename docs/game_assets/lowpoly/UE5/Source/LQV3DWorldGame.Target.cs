# LQV3DWorld — UE5 game target
using UnrealBuildTool;

TargetRules = new TargetRules[]
{
    new TargetRules(TargetType.Game, "LQV3DWorldTarget")
};

ModuleRules = new ModuleRules[]
{
    new ModuleRules("LQV3DWorld")
};

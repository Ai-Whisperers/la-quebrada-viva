# LQV3DWorld — UE5 editor target
using UnrealBuildTool;

TargetRules = new TargetRules[]
{
    new TargetRules(TargetType.Editor, "LQV3DWorldEditorTarget")
};

ModuleRules = new ModuleRules[]
{
    new ModuleRules("LQV3DWorld")
};

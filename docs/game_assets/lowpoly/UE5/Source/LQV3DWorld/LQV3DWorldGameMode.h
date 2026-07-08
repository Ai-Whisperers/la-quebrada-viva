// LQV3DWorld — basic GameMode header.
// Real input bindings, player controller, etc. live here when wired.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "LQV3DWorldGameMode.generated.h"

UCLASS()
class LQV3DWORLD_API ALQV3DWorldGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ALQV3DWorldGameMode();
};

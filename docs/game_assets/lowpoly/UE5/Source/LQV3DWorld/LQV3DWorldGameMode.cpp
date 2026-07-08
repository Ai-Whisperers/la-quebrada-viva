#include "LQV3DWorldGameMode.h"

ALQV3DWorldGameMode::ALQV3DWorldGameMode()
{
    // Default pawn is the LQV3DWorldCharacter (third-person walk + click-to-place)
    DefaultPawnClass = nullptr;  // set in Blueprint subclass
}

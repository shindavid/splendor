#include <cstdint>
#include <cstring>
#include <initializer_list>
#include <string>

struct StandardGameSpecs {
  enum Color {
    eWhite,
    eBlue,
    eGreen,
    eRed,
    eBlack,
    eGold
  } __attribute__((packed));

  static char toChar(Color pC) {
    return "WUGRBJ"[pC];
  }

  static const uint8_t sNumLevels = 3;
  static const uint8_t sNumBaseColors = 5;
  static const uint8_t sNumAllColors = sNumBaseColors+1;
  static const uint8_t sNumGolds = 5;
  static const uint8_t sNumDisplayedCardsPerLevel = 5;
  static const uint8_t sPerPlayerCoinLimit = 10;
  static const uint8_t sNumCoinsToTakePerTurn = 3;
  static const uint8_t sRequiredStackSizeToTakeTwo = 4;
  static const uint8_t sReservedCardLimit = 3;
  static const uint8_t sGameEndingScore = 15;

  class CoinSet {
  private:
    uint8_t mCounts[sNumAllColors] = {};

  public:
    CoinSet() {}
    CoinSet(const std::initializer_list<uint8_t>& pCounts) {
      int lIndex = 0;
      for (uint8_t lCount : pCounts) mCounts[lIndex++] = lCount;
    }

    uint8_t& operator[](Color pC) { return mCounts[pC]; }
    const uint8_t& operator[](Color pC) const { return mCounts[pC]; }

    std::string toString() const {
      char lBuffer[64];
      char* lPtr = lBuffer;
      for (int i=0; i< sNumAllColors; ++i) {
        if (!mCounts[i]) continue;
        lPtr += sprintf(lPtr, "%d%c,", (int)mCounts[i], toChar((Color)i));
      }
      *lPtr = '\0';
      return std::string(lBuffer);
    }
  } __attribute__((packed));

  struct Card {
    const CoinSet mCost;
    const uint8_t mID;
    const Color mColor : 3;
    const uint8_t mPoints : 3;
    const uint8_t mLevel : 2;  // 0-indexed for convenience

    Card(uint8_t pID, const CoinSet& pCost, uint8_t pPoints, uint8_t pLevel, Color pColor) :
      mCost(pCost), mID(pID), mColor(pColor), mPoints(pPoints), mLevel(pLevel) {}

    std::string toString() const {
      char lBuffer[128];
      sprintf(lBuffer, "%d:%d%c%d[%s]", (int)mID, (int)mLevel, toChar(mColor), (int)mPoints,
          mCost.toString().c_str());
      return std::string(lBuffer);
    };
  };
  static_assert(sizeof(Card) <= 8, "Oversized Card object");

  static const Card sCardList[];

  struct Noble {
    const CoinSet mRequirement;
    const uint8_t mID;
    const uint8_t mPoints;

    Noble(uint8_t pID, uint8_t pPoints, const CoinSet& pRequirement) :
      mRequirement(pRequirement), mID(pID), mPoints(pPoints) {}

    std::string toString() const {
      char lBuffer[64];
      sprintf(lBuffer, "%d:%d[%s]", (int)mID, (int)mPoints, mRequirement.toString().c_str());
      return std::string(lBuffer);
    }
  };
  static_assert(sizeof(Noble) <= 8, "Oversized Noble object");

  static const Noble sNobleList[];
};


namespace TofuyaGame;

public class GameState
{
    // constants for business rules
    public const int goal = 100000;
    public const int costPerBlock = 50;
    public const int pricePerBlock = 150;

    // current status
    public int currentMoney { get; set; } = 5000;
    public int day { get; set; } = 1;
    public string currentWeather { get; set; } = "Clear";

    public bool isGameOver => currentMoney < costPerBlock || currentMoney >= goal;
    public bool isVictory => currentMoney > goal;
}
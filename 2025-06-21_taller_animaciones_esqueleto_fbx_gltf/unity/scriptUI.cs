using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class UIAnimationController : MonoBehaviour
{
    public Animator animator;
    public TMP_Dropdown animationDropdown;
    
    private string currentAnimation = "Drunk Idle Variation";

    void Start()
    {
        animationDropdown.onValueChanged.AddListener(ChangeAnimation);
    }

    public void PauseAnimation()
    {
        animator.speed = 0;
    }

    public void ResumeAnimation()
    {
        animator.speed = 1;
    }

    public void RestartAnimation()
    {
        animator.Play(currentAnimation, 0, 0f);
    }

    public void ChangeAnimation(int index)
    {
        switch (index)
        {
            case 0:
                currentAnimation = "Drunk Idle Variation";
                break;
            case 1:
                currentAnimation = "Illegal Elbow Punch";
                break;
            case 2:
                currentAnimation = "Standing Idle To Fight Idle";
                break;
        }

        animator.Play(currentAnimation);
    }
}

using UnityEngine;

public class UIAnimationTrigger : MonoBehaviour
{
    public Animator animator;

    public void TriggerWave() => animator.SetTrigger("WaveTrigger");
    public void TriggerJump() => animator.SetTrigger("JumpTrigger");
    public void ToggleWalk() => animator.SetBool("IsWalking", !animator.GetBool("IsWalking"));
}

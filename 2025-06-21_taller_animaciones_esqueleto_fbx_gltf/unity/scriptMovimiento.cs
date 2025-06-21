using UnityEngine;

public class CharacterAnimationController : MonoBehaviour
{
    Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
            animator.Play("Drunk Idle Variation");

        if (Input.GetKeyDown(KeyCode.Alpha2))
            animator.Play("Illegal Elbow Punch");

        if (Input.GetKeyDown(KeyCode.Alpha3))
            animator.Play("Standing Idle To Fight Idle");
    }
}

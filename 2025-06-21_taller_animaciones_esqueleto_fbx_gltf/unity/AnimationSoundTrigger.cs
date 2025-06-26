using UnityEngine;

public class AnimationSoundTrigger : MonoBehaviour
{
    public AudioSource audioSource;
    public AudioClip jumpSound;

    public void PlayJumpSound()
    {
        audioSource.PlayOneShot(jumpSound);
    }
}

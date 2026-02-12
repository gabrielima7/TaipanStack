"""
GPG Signature Validation.
"""
import gnupg
from taipanstack.core.result import Err, Ok, Result

# Initialize GPG.
# We might need a homedir for keyring, or just use verify(data) with inline keys if supported,
# but usually we import key then verify.
# For simplicity in this containerized env, we can use a temp keyring or default.
# Initialize GPG.
# Setting homedir to /tmp/gnupg to ensure write access for temporary keyring.
import os
gnupg_home = "/tmp/gnupg"
if not os.path.exists(gnupg_home):
    os.makedirs(gnupg_home, mode=0o700)
gpg = gnupg.GPG(gnupghome=gnupg_home)

def verify_signature(content: str, signature: str, public_key: str) -> Result[bool, str]:
    """Verify GPG signature against content using provided public key.

    Args:
        content: The raw body content (string).
        signature: The detached signature (ASCII armored).
        public_key: The signer's public key (ASCII armored).

    Returns:
        Ok(True) if valid.
        Err(reason) if invalid.
    """
    try:
        # Import key to temp keyring
        import_result = gpg.import_keys(public_key)
        if import_result.count == 0:
            return Err("Invalid Public Key format")

        # Create temp file for content
        # verify_file is more reliable for detached signatures in python-gnupg
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Verify using file path
            # signature is the detached signature string (ASCII armored)
            # data_filename points to the content file
            import io
            # We must convert signature string to bytes stream if verify_file expects stream
            # or pass it as first arg if verify_file handles it?
            # python-gnupg verify_file(file, data_filename=None, sig_file=None)
            # file is the signature file stream.

            sig_stream = io.BytesIO(signature.encode('utf-8'))
            verified = gpg.verify_file(sig_stream, data_filename=tmp_path)

            if verified.valid:
                return Ok(True)
            else:
                return Err(f"Signature Invalid: {verified.status} - {verified.problems}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        return Err(f"GPG Error: {str(e)}")

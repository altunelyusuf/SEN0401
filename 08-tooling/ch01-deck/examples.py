# Every computation the SEN0401 chapter 1 deck shows. Outputs are produced by executing these under the
# current Python at build time, never typed.
EX = {
 "pow": ["import hashlib; nonce = next(n for n in range(10**6) if hashlib.sha256(f'SEN0401-{n}'.encode()).hexdigest().startswith('0000')); nonce",
         "hashlib.sha256(f'SEN0401-{nonce}'.encode()).hexdigest()[:24]"],
 "supply": ["sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8", "(50 * 10**8 >> 4) / 10**8"],
 "eras": ["[(50 * 10**8 >> era) / 10**8 for era in range(6)]"],
}

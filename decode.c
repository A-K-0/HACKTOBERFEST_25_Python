int numDecodings(char *s) {
    int n = strlen(s);
    if (n == 0 || s[0] == '0')
        return 0;

    int dp_prev2 = 1;  // dp[i-2]
    int dp_prev1 = 1;  // dp[i-1]

    for (int i = 1; i < n; i++) {
        int dp_current = 0;

        // Case 1: Single digit decode (must not be '0')
        if (s[i] != '0') {
            dp_current += dp_prev1;
        }

        // Case 2: Two-digit decode (10 to 26)
        int twoDigit = (s[i - 1] - '0') * 10 + (s[i] - '0');
        if (twoDigit >= 10 && twoDigit <= 26) {
            dp_current += dp_prev2;
        }

        // If no valid decoding
        if (dp_current == 0)
            return 0;

        dp_prev2 = dp_prev1;
        dp_prev1 = dp_current;
    }

    return dp_prev1;
}

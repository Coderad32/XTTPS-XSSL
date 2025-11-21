# client.pl
use strict;
use warnings;
use IO::Socket::INET;
use XTTP::Message;

my $hmac_key = 'supersecret'; # match server's for demo

my $sock = IO::Socket::INET->new(
    PeerAddr => '127.0.0.1',
    PeerPort => 8088,
    Proto    => 'tcp',
) or die "Connect failed: $!";

my $msg = XTTP::Message->new(
    method  => 'SEND',
    path    => '/ping',
    headers => { 'Content-Type' => 'text/plain' },
    body    => 'ping',
    hmac_key => $hmac_key,
);

print $sock $msg->serialize;

# Read response
my $resp = '';
while (my $line = <$sock>) {
    $resp .= $line;
    last if $line =~ /^HMAC:/; # simplistic read for demo
}
close $sock;

my $parsed = XTTP::Message->parse($resp, hmac_key => $hmac_key);
print "Status: $parsed->{headers}{Status}\n";
print "Body: $parsed->{body}\n";
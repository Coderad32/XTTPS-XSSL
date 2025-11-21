# server.pl
use strict;
use warnings;
use IO::Socket::INET;
use XTTP::Message;

my $hmac_key = 'supersecret'; # replace with proper key management

my $server = IO::Socket::INET->new(
    LocalAddr => '0.0.0.0',
    LocalPort => 8088,
    Proto     => 'tcp',
    Listen    => 5,
    Reuse     => 1,
) or die "Could not start server: $!";

print "XTTP server listening on 0.0.0.0:8088\n";

while (my $client = $server->accept) {
    $client->autoflush(1);

    # Read until we can parse headers and body length
    my $buf = '';
    while ($buf !~ /\r\n\r\n/) {
        my $read = <$client>;
        last unless defined $read;
        $buf .= $read;
    }
    # Extract Content-Length to read body
    my ($headers) = $buf =~ /\A.*?\r\n\r\n/s;
    my ($len) = $headers =~ /^Content-Length:\s*(\d+)/mi;
    $len ||= 0;

    my $body = '';
    read($client, $body, $len) if $len > 0;
    $buf .= $body;

    # Optionally read HMAC trailer line
    my $line = <$client>;
    $buf .= $line if defined $line;

    my $msg;
    eval { $msg = XTTP::Message->parse($buf, hmac_key => $hmac_key) };
    if ($@) {
        print $client "SEND /error xttp/1.0\r\nStatus: 400\r\nContent-Length: 0\r\n\r\n";
        close $client;
        next;
    }

    # Application logic
    my $reply_body = "ok";
    my $reply = XTTP::Message->new(
        method  => 'REPLY',
        path    => $msg->{path},
        headers => { Status => 200, 'Content-Type' => 'text/plain' },
        body    => $reply_body,
        hmac_key => $hmac_key,
    );

    print $client $reply->serialize;
    close $client;
}